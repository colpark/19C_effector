#!/usr/bin/env python3
"""Build the functionally validated fungal/oomycete effector sequence union."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import re
import tarfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
PEACE_COMMIT = "90b8fc902f0b444e7f21adf75dae41a05931cc5f"
PREDECTOR_COMMIT = "3d2a591fadbe7c398c1ac398371b3b2610a60d46"
PHIBASE_RELEASE = "4.19"
ALLOWED_AA = set("ACDEFGHIKLMNPQRSTVWYBXZJUO")


def normalize_sequence(value: str) -> str:
    sequence = re.sub(r"\s+", "", value).upper().replace("*", "")
    if not sequence or set(sequence) - ALLOWED_AA:
        return ""
    return sequence


def read_fasta(path: Path) -> Iterable[tuple[str, str]]:
    name = None
    parts: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith(">"):
                if name is not None:
                    yield name, normalize_sequence("".join(parts))
                name, parts = line[1:], []
            elif line:
                parts.append(line)
    if name is not None:
        yield name, normalize_sequence("".join(parts))


def taxonomy_parents(path: Path) -> dict[int, int]:
    with tarfile.open(path, "r:gz") as archive:
        member = archive.extractfile("nodes.dmp")
        if member is None:
            raise ValueError("NCBI taxdump lacks nodes.dmp")
        parents = {}
        for raw in io.TextIOWrapper(member, encoding="utf-8"):
            fields = [field.strip() for field in raw.split("|")]
            parents[int(fields[0])] = int(fields[1])
        return parents


def is_descendant(taxid: int, ancestors: set[int], parents: dict[int, int]) -> bool:
    seen = set()
    while taxid not in seen and taxid in parents:
        if taxid in ancestors:
            return True
        seen.add(taxid)
        parent = parents[taxid]
        if parent == taxid:
            return False
        taxid = parent
    return taxid in ancestors


def infer_lifestyle(organism: str, entry_kind: str = "") -> str:
    text = f"{organism} {entry_kind}".lower()
    if "necrotroph" in text or any(name in text for name in (
            "botrytis", "sclerotinia", "parastagonospora", "pyrenophora",
            "bipolaris", "cochliobolus")):
        return "necrotroph"
    if any(name in text for name in (
            "blumeria", "puccinia", "melampsora", "ustilago", "cladosporium fulvum",
            "fulvia fulva")):
        return "biotroph"
    if any(name in text for name in (
            "phytophthora", "magnaporthe", "fusarium", "colletotrichum",
            "leptosphaeria", "verticillium", "zymoseptoria")):
        return "hemibiotroph"
    return "unknown"


def q4_from_record(entry_kind: str, text: str, experiment: str) -> str:
    combined = f"{entry_kind} {text}".lower()
    if "avirulence" in combined or "map-based" in combined or "forward genetic" in combined:
        return "yes"
    if experiment == "knockout virulence phenotype":
        return "yes"
    if any(term in combined for term in ("effectorp", "effhunter", "wideeffhunter",
                                         "small secreted", "cysteine-rich screen")):
        return "no"
    return "unknown"


def year_from_text(value: str) -> str:
    years = [int(item) for item in re.findall(r"(?:19|20)\d{2}", value)]
    return str(min(years)) if years else "unknown"


def evidence_from_predector(row: dict[str, str]) -> tuple[str, str] | None:
    entry_kind = row["entry_kind"].lower()
    notes = row["notes"].lower()
    go_terms = row["go_terms"].lower()
    phi_terms = row["phibase_terms"].lower()
    if ("avirulence" in entry_kind or "hypersensitive" in go_terms
            or "triggers hr" in notes or "recognised by" in notes):
        return "hypersensitive response assay", "Predector literature record"
    if any(term in phi_terms for term in (
            "loss of pathogenicity", "reduced virulence", "increased virulence",
            "gain of pathogenicity")):
        return "knockout virulence phenotype", "Predector/PHI-base phenotype record"
    if ("interact" in notes or "effector mediated modulation" in phi_terms
            or "host target" in notes):
        return "validated host-target interaction", "Predector literature record"
    return None


def evidence_from_phibase(rows: list[dict[str, str]]) -> tuple[str, str, str] | None:
    for row in rows:
        phenotype = row["Phenotype_of_mutant"].lower()
        host_response = row["Host_response"].lower()
        experiment = row["Experimental_evidence"].lower()
        interaction = row["Interaction phenotype"].lower()
        host_target = row["Tested Host_target"].strip()
        transient = row["Transient Assay Experimental Evidence"].lower()
        if "effector (plant avirulence determinant)" in phenotype or "hypersensitive" in host_response:
            return ("hypersensitive response assay",
                    row["Experimental_evidence"] or row["Transient Assay Experimental Evidence"],
                    row["Year_published"] or year_from_text(row["Full_citation"]))
        if (any(term in phenotype for term in ("loss of pathogenicity", "reduced virulence"))
                and any(term in experiment for term in (
                    "deletion", "mutation", "disruption", "silencing"))):
            return ("knockout virulence phenotype", row["Experimental_evidence"],
                    row["Year_published"] or year_from_text(row["Full_citation"]))
        positive_interaction = any(term in interaction for term in (
            "binding", "positive", "interacts", "interaction"))
        assay_interaction = any(term in transient for term in (
            "co-ip", "bifc", "split yfp", "yeast two-hybrid", "co-expression"))
        if host_target and (positive_interaction or assay_interaction):
            return ("validated host-target interaction",
                    row["Interaction phenotype"] or row["Transient Assay Experimental Evidence"],
                    row["Year_published"] or year_from_text(row["Full_citation"]))
    return None


def first_identifier(row: dict[str, str]) -> str:
    for field in ("uniprot", "genbank", "phibase", "gene"):
        value = row.get(field, "").strip()
        if value:
            return re.split(r"[;|]", value)[0].strip()
    return "unnamed"


def safe_identifier(value: str) -> str:
    result = re.sub(r"[^A-Za-z0-9_.:-]+", "_", value.strip()).strip("_")
    return result or "unnamed"


def load_uniprot(paths: list[Path]) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    by_accession = {}
    by_sequence = {}
    for path in paths:
        with gzip.open(path, "rt", encoding="utf-8") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                sequence = normalize_sequence(row["Sequence"])
                by_accession[row["Entry"]] = row
                if sequence:
                    by_sequence.setdefault(sequence, row)
    return by_accession, by_sequence


def add_record(records: dict[str, dict[str, Any]], sequence: str, *, accession: str,
               source: str, release: str, organism: str, lifestyle: str,
               year: str, evidence: str, experiment: str, q4: str) -> None:
    if not sequence:
        return
    record = records.setdefault(sequence, {
        "accessions": set(), "sources": set(), "releases": set(), "organisms": set(),
        "lifestyles": set(), "years": set(), "evidence": set(), "experiments": set(),
        "q4": set(),
    })
    record["accessions"].add(accession)
    record["sources"].add(source)
    record["releases"].add(release)
    if organism:
        record["organisms"].add(organism)
    if lifestyle:
        record["lifestyles"].add(lifestyle)
    if year:
        record["years"].add(year)
    record["evidence"].add(evidence)
    if experiment:
        record["experiments"].add(experiment)
    record["q4"].add(q4)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--peace-dir", type=Path, required=True)
    parser.add_argument("--predector", type=Path, required=True)
    parser.add_argument("--phibase-csv", type=Path, required=True)
    parser.add_argument("--phibase-fasta", type=Path, required=True)
    parser.add_argument("--taxdump", type=Path, required=True)
    parser.add_argument("--uniprot", type=Path, action="append", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    parents = taxonomy_parents(args.taxdump)
    uniprot_by_accession, uniprot_by_sequence = load_uniprot(args.uniprot)
    records: dict[str, dict[str, Any]] = {}
    summaries: dict[str, dict[str, int]] = {}

    predector_rows = []
    with args.predector.open(encoding="utf-8", newline="") as handle:
        predector_rows = list(csv.DictReader(handle, delimiter="\t"))
    predector_sequences = set()
    predector_retained = set()
    for row in predector_rows:
        sequence = normalize_sequence(row["sequence"])
        if not sequence or row["kingdom"] not in {"fungi", "protista"}:
            continue
        predector_sequences.add(sequence)
        evidence = evidence_from_predector(row)
        if evidence is None:
            continue
        accession = first_identifier(row)
        organism = row["organism"]
        year = year_from_text(f"{row['references']} {row['reference_urls']}")
        q4 = q4_from_record(row["entry_kind"], f"{row['notes']} {row['names']}", evidence[0])
        add_record(records, sequence, accession=accession, source="Predector confirmed set",
                   release=PREDECTOR_COMMIT, organism=organism,
                   lifestyle=infer_lifestyle(organism, row["entry_kind"]), year=year,
                   evidence=evidence[0], experiment=evidence[1], q4=q4)
        predector_retained.add(sequence)
    summaries["Predector confirmed set"] = {
        "candidate_sequences": len(predector_sequences),
        "retained_sequences": len(predector_retained),
        "removed_sequences": len(predector_sequences - predector_retained),
    }

    phi_by_accession: dict[str, list[dict[str, str]]] = defaultdict(list)
    phi_fields = (
        "Function", "Phenotype_of_mutant", "Host_response", "Experimental_evidence",
        "Transient Assay Experimental Evidence", "Interaction phenotype",
        "Tested Host_target", "Year_published", "Full_citation", "Pathogen_species",
    )
    with args.phibase_csv.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            accession = row["ProteinID"].strip()
            if accession:
                phi_by_accession[accession].append({field: row[field] for field in phi_fields})
    phi_candidates = set()
    phi_retained = set()
    for header, sequence in read_fasta(args.phibase_fasta):
        fields = [field.strip() for field in header.split("#")]
        if len(fields) < 6 or not sequence:
            continue
        accession, _, gene, taxid_text, organism_text, phenotype = fields[:6]
        accession = accession.strip()
        try:
            taxid = int(taxid_text)
        except ValueError:
            continue
        if not is_descendant(taxid, {4751, 4762}, parents):
            continue
        rows = phi_by_accession.get(accession, [])
        function_text = " ".join(row["Function"] for row in rows).lower()
        if "effector" not in function_text and "effector" not in phenotype.lower():
            continue
        phi_candidates.add(sequence)
        evidence = evidence_from_phibase(rows)
        if evidence is None:
            continue
        organism = rows[0]["Pathogen_species"] if rows else organism_text.replace("_", " ")
        entry_text = f"{gene} {phenotype} {function_text}"
        add_record(records, sequence, accession=accession, source="PHI-base",
                   release=f"v{PHIBASE_RELEASE}", organism=organism,
                   lifestyle=infer_lifestyle(organism), year=evidence[2] or "unknown",
                   evidence=evidence[0], experiment=evidence[1],
                   q4=q4_from_record(entry_text, entry_text, evidence[0]))
        phi_retained.add(sequence)
    summaries["PHI-base"] = {
        "candidate_sequences": len(phi_candidates),
        "retained_sequences": len(phi_retained),
        "removed_sequences": len(phi_candidates - phi_retained),
    }

    peace_sources: dict[str, set[str]] = defaultdict(set)
    positive_dir = args.peace_dir / "src/data/dataset_construction/positive_seqs"
    for path in sorted(positive_dir.glob("*.fasta")):
        source_name = path.stem
        for _, sequence in read_fasta(path):
            if sequence:
                peace_sources[sequence].add(source_name)
    peace_retained = set()
    for sequence, sources in peace_sources.items():
        if sequence not in records:
            continue
        record = records[sequence]
        record["sources"].add("PEACE curated positives")
        record["releases"].add(PEACE_COMMIT)
        record["experiments"].add("PEACE source memberships: " + ";".join(sorted(sources)))
        if any("effectorp" in source.lower() or "effhunter" in source.lower()
               for source in sources) and "yes" not in record["q4"]:
            record["q4"].add("no")
        peace_retained.add(sequence)
    summaries["PEACE curated positives"] = {
        "candidate_sequences": len(peace_sources),
        "retained_sequences": len(peace_retained),
        "removed_sequences": len(set(peace_sources) - peace_retained),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    fasta_path = args.output_dir / "union.fasta"
    provenance_path = args.output_dir / "provenance.tsv"
    used_accessions: dict[str, int] = defaultdict(int)
    rows = []
    fasta_chunks = []
    for sequence, record in sorted(records.items(), key=lambda item: (sorted(item[1]["accessions"])[0], item[0])):
        accession = safe_identifier(sorted(record["accessions"])[0])
        used_accessions[accession] += 1
        if used_accessions[accession] > 1:
            accession = f"{accession}__{used_accessions[accession]}"
        uniprot = uniprot_by_accession.get(accession) or uniprot_by_sequence.get(sequence)
        organisms = {value for value in record["organisms"] if value and value != "unknown"}
        if uniprot and uniprot.get("Organism"):
            organisms.add(uniprot["Organism"])
        lifestyles = {value for value in record["lifestyles"] if value != "unknown"}
        q4_values = record["q4"]
        q4 = "yes" if "yes" in q4_values else ("no" if "no" in q4_values else "unknown")
        years = sorted(value for value in record["years"] if value != "unknown")
        cysteines = sequence.count("C")
        fasta_chunks.append(f">{accession}\n{sequence}\n")
        rows.append({
            "accession": accession,
            "source_database": "; ".join(sorted(record["sources"])),
            "source_release": "; ".join(sorted(record["releases"])),
            "organism": "; ".join(sorted(organisms)) or "unknown",
            "lifestyle": "; ".join(sorted(lifestyles)) or "unknown",
            "length": len(sequence),
            "cysteine_count": cysteines,
            "cysteine_fraction": f"{cysteines / len(sequence):.6f}",
            "publication_year": years[0] if years else "unknown",
            "functional_evidence": "; ".join(sorted(record["evidence"])),
            "experiment": "; ".join(sorted(record["experiments"])),
            "q4_tool_independent": q4,
            "sequence_sha256": hashlib.sha256(sequence.encode()).hexdigest(),
        })
    fasta_path.write_text("".join(fasta_chunks), encoding="utf-8")
    fieldnames = list(rows[0]) if rows else []
    with provenance_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    q4_counts = {value: sum(row["q4_tool_independent"] == value for row in rows)
                 for value in ("yes", "no", "unknown")}
    summary = {
        "sources": summaries,
        "union_retained_sequences": len(rows),
        "q4_tool_independent": q4_counts,
        "functional_evidence_counts": {
            value: sum(value in row["functional_evidence"] for row in rows)
            for value in ("hypersensitive response assay", "knockout virulence phenotype",
                          "validated host-target interaction")
        },
    }
    (args.output_dir / "curation_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
