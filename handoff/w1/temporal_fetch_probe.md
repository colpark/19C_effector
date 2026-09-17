# Temporal Fetcher condition probe

The temporal condition was **not executed**. The fail-closed wrapper was invoked without
`--execute` to verify that it will not move any target without an explicit repository,
credential file, offline directory, and external Fetcher command. Its verbatim output was:

```text
usage: copy script outside repo; scripts/temporal_fetch.sh --execute --repo REPO --credentials FILE --offline-root DIR -- FETCHER_COMMAND...
EXIT=2
```

Execution is blocked before partial satisfaction: the Fetcher launcher retains its independent
preparation-host refusal even if the union tree is moved away, and no external role session is
available. Moving the repository and credentials first would not yield an admissible Fetcher
retrieval. No absence probes of moved paths exist because nothing was moved; treating this usage
check as an absence verification would be false.
