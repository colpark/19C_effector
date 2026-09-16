# Structural-channel exclusions

The Curator runtime boundary is failed. No claim from this artifact is admissible
until that boundary holds.

## Rule

The carded reused ESMFold wrapper accepts only canonical amino-acid sequences of
at most 600 residues. The residual runner therefore applied two **hard input
cutoffs**, not a wall-clock decision: sequence length `>600` residues, or any
residue outside `ACDEFGHIKLMNPQRSTVWY`. The rule was committed in `5763377`.

The 18 length exclusions begin at 605 aa; the longest included valid residual
sequence is 580 aa. `H1VSQ9` is an additional 170-aa exclusion because it
contains `X`, which the carded wrapper rejects. Thus the effective length gap
is 580–605 aa, but the full exclusion rule also has an alphabet condition.

## Excluded records

| Accession | Length | profile_stratum | lifestyle | Source organism | Rule |
|---|---:|---|---|---|---|
| A0A0D1CZH2 | 780 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1DMZ9 | 742 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1DYI3 | 869 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1E1G8 | 626 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1E3H5 | 703 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1E5A8 | 709 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| A0A0D1E997 | 605 | non-canonical | biotroph | Ustilago maydis | >600 aa carded limit |
| E3KIN4 | 820 | non-canonical | biotroph | Puccinia graminis f. sp. tritici | >600 aa carded limit |
| E3L2L4 | 744 | non-canonical | biotroph | Puccinia graminis f. sp. tritici | >600 aa carded limit |
| E4ZUN5 | 658 | non-canonical | hemibiotroph | Leptosphaeria maculans | >600 aa carded limit |
| E6ZPZ7 | 612 | non-canonical | unknown | Sporisorium reilianum | >600 aa carded limit |
| E6ZS79 | 1464 | non-canonical | unknown | Sporisorium reilianum | >600 aa carded limit |
| E7A0K5 | 773 | non-canonical | unknown | Sporisorium reilianum | >600 aa carded limit |
| G2XWG3 | 852 | non-canonical | necrotroph | Botrytis cinerea | >600 aa carded limit |
| G4YIB3 | 1715 | non-canonical | hemibiotroph | Phytophthora sojae | >600 aa carded limit |
| H1VSQ9 | 170 | canonical | hemibiotroph | Colletotrichum higginsianum | noncanonical `X` rejected by carded wrapper |
| Q6ZX14 | 4034 | non-canonical | hemibiotroph | Magnaporthe oryzae; Pyricularia oryzae | >600 aa carded limit |
| R0J3Y1 | 785 | non-canonical | unknown | Exserohilum turcicum | >600 aa carded limit |
| R0KGT7 | 993 | non-canonical | unknown | Exserohilum turcicum | >600 aa carded limit |

Eighteen of nineteen exclusions are non-canonical. `H1VSQ9` disproves the
claim that every exclusion is non-canonical; it is a canonical sequence with
an invalid residue symbol.
