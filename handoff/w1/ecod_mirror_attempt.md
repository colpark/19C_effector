# Item 58 — ECOD mirror attempt from Fetcher scope

No claim from this artifact is admissible until the runtime boundary holds.

The rendered Fetcher clone attempted this public GitHub mirror candidate before any
substitution ruling:

```bash
curl -L --fail --silent --show-error --connect-timeout 20 \
  https://raw.githubusercontent.com/biocryst/ecod/main/ecod.latest.domains.txt \
  -o /tmp/ecod_mirror.txt
```

Verbatim result:

```text
curl: (22) The requested URL returned error: 404
mirror_curl_exit=22
```

No ECOD mirror data were used, so no retrieval date or checksum exists. Together with
the official-endpoint connection refusal, this supports the Referee's conditional
SCOP authorization rather than an unrecorded source substitution.
