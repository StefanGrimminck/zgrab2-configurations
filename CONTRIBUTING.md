# Contributing

The goal is a set of ZGrab2 configs that are accurate, specific about what they
detect, and safe to run. CI enforces the mechanical rules below on every push
and pull request.

## Standard requests only

These configs follow the ethics note in the
[ZGrab2 README](https://github.com/zmap/zgrab2#readme):

> ZGrab will only collect information that is available to any standard
> application client _without_ authenticating. We will not accept contributions
> that attempt to gain access to systems by exploiting vulnerabilities or
> attempting to brute-force credentials.

A probe sends one request that an ordinary client would send: a GET or HEAD for
a page, file or API the service offers to anyone, or the handshake a ZGrab2
module performs. It never exploits a vulnerability to get there. That rules
out path traversal and encoded separators, path-parameter or header tricks
that skip an access check, injected arguments or expressions, deserialization
payloads, out-of-band callbacks, and credential guessing. `tools/lint.py`
rejects the patterns it can recognise; review catches the rest.

A CVE probe therefore covers its CVE by fingerprint. It identifies the affected
product and, where the service publishes it to any visitor, the version or
build, and its comment gives the affected range so the reader can compare.
When a product shows no version without authentication, the probe identifies
the product and says that the version has to be checked another way.

## Where a config goes

- `base-configurations/` holds one file per ZGrab2 module, with the module's
  options listed as comments. Add one only for a new upstream module, and add
  it to `all.ini` and `all_trigger-on-port.ini`.
- `service-discovery/` fingerprints a specific product on its usual port.
- `vulnerabilities/misconfigurations/` detects a dangerous default, an exposed
  file or an unauthenticated API.
- `vulnerabilities/cve/` fingerprints a product affected by a specific CVE.

## Specific, not hopeful

A product-named probe must be strongly specific. The port and request path
together have to point at that product, not at anything that happens to answer
on that port. Do not label a generic response from `/`, `/health`, `/healthz`,
`/login` or a generic API path as a particular product when another
application could return the same thing.

ZGrab2 records the response but does not assert on it, so the comment names the
marker that proves a hit (a header, a JSON field, a page title) and the reader
confirms it in the output.

## File format

Every config in `service-discovery/` and `vulnerabilities/` starts with a
comment block, then the module section:

```ini
# What the product is, why this port and path identify it, and the response
# marker to confirm. One tight paragraph about the target, nothing about the
# probe itself or how it was written.
[http]
name="product-name"
port=1234
endpoint="/distinctive/path"

# A short note for each option the probe sets.
retry-https=true
max-size=16
```

- `name=` is lowercase letters, digits and hyphens, unique across the
  repository, and usually matches the filename.
- Files in `vulnerabilities/cve/` name their CVE on the first line, as
  `# CVE-YYYY-NNNNN  -  ...`, and are named `product-CVE-YYYY-NNNNN.ini`.
- Set only the options the probe uses. Boolean options are written
  `option=true`, never as a bare key.
- Run `zgrab2 <module> --help` to confirm option names, which change between
  ZGrab2 releases.

## Before you open a pull request

```bash
python3 tools/lint.py          # conventions and the standard-request rules
python3 tools/catalog.py       # regenerate CATALOG.md from the configs
printf '127.0.0.1\n' | zgrab2 -b /dev/null multiple -c path/to/your.ini -o /dev/null
```

A clean parse means ZGrab2 accepts the file. It does not prove the probe
identifies a live service, so where you can, run it against a real instance
(a container is usually enough) and say in the comment what you checked.

## Writing

Plain prose in comments, docs and commit messages. No em-dashes, unicode arrows
or curly quotes; CI rejects them.
