# Contributing

Thanks for helping improve this collection. The goal is a set of ZGrab2 configs
that are accurate, honest about what they detect, and safe to run. A few
conventions keep it that way, and CI enforces the mechanical ones on every push
and pull request.

## Where a config goes

- `base-configurations/` holds one file per ZGrab2 module. Add here only for a
  new protocol module.
- `service-discovery/` fingerprints a specific product on its usual port.
- `vulnerabilities/misconfigurations/` detects a dangerous default or exposure.
- `vulnerabilities/exploitation/` detects a host vulnerable to a specific CVE.

## The one rule that matters most

A product-named probe must be strongly specific. The port and request path
together have to point at that product, not at anything that happens to answer on
that port. Do not label a generic response from `/`, `/health`, `/healthz`,
`/login`, or a generic API path as a particular product when another application
could plausibly return the same thing. If the only thing making a probe
"product X" is the port, it is too weak.

ZGrab2 records the response but does not assert on the body from these files, so
your comment should name the response marker a user can confirm in the output
(a header, a JSON field, a page title). Say what proves the hit.

## Detection only

Configs under `vulnerabilities/` detect a vulnerable endpoint or read a single
known indicator. They do not execute code, send a working exploit, or depend on
an out-of-band callback to confirm a result. If a vulnerability can only be
confirmed by exploiting it or by catching a callback, it does not belong here.

## File format

Every config in `service-discovery/` and `vulnerabilities/` starts with a comment
block, then the module section:

```ini
# What the product is, why this port and path identify it, and the response
# marker to confirm. One tight paragraph.
[http]
name="product-name"
port=1234
endpoint="/distinctive/path"

# Only the options this probe actually needs, with a short note each.
retry-https=true
max-size=16
```

- `name=` is lowercase letters, digits, and hyphens, and is unique across the
  repository. It usually matches the filename.
- Every file in `vulnerabilities/exploitation/` names its CVE on the first line,
  as `# CVE-YYYY-NNNNN  -  ...`.
- Boolean options are written `option=true`, not as a bare key.
- Run `zgrab2 <module> --help` to confirm current option names before relying on
  them, since some have changed across ZGrab2 releases.

## Writing

Plain prose in comments, docs, and commit messages. No em-dashes (use a hyphen or
a comma), no unicode arrows or curly quotes. CI rejects these.

## Before you open a pull request

CI builds upstream ZGrab2 and loads every INI, and separately checks the
conventions above. To mirror it locally, build ZGrab2 and parse your file:

```bash
printf '127.0.0.1\n' | zgrab2 -b /dev/null multiple -c path/to/your.ini -o /dev/null
```

A clean parse means the config is well formed. It does not by itself confirm the
probe identifies a live remote service, so where you can, verify the expected
response marker against a real instance and note it in the comment.
