# Item 54 — ECOD retrieval from Fetcher scope

The ECOD block is external, not a consequence of the Instrument's empty network
allowlist. No claim from this artifact is admissible until the runtime boundary holds.

The Fetcher profile was amended to allow `prodata.swmed.edu`, rendered into a fresh
standalone Fetcher clone at `/tmp/effector-fetcher-ecod-20260916`, and its rendered
policy had `network_access: true`, `strictAllowlist: true`, and that host in
`allowedDomains`. The role runtime boundary remains failed, so this is evidence of the
configured Fetcher policy plus a direct retrieval, not proof of an enforced sandbox.

Command:

```bash
curl -L --fail --silent --show-error --connect-timeout 20 \
  https://prodata.swmed.edu/ecod/complete/ecod.latest.domains.txt \
  -o /tmp/ecod.latest.domains.txt
```

Verbatim result:

```text
curl: (7) Failed to connect to prodata.swmed.edu port 443 after 277 ms: Couldn't connect to server
curl_exit=7
```

The external holder remains the ECOD data service. Clause 14 does not move this row:
the configured role permission was supplied and the remaining remedy requires the
outside service to become reachable or publish an alternate official endpoint.
