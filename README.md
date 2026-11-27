# ZGrab2 configurations

*Honeypot-informed scan configs for [ZGrab2](https://github.com/zmap/zgrab2): service discovery, misconfiguration checks, and CVE fingerprints.*

[![Validate ZGrab2 configurations](https://github.com/StefanGrimminck/zgrab2-configurations/actions/workflows/validate-zgrab2-configs.yml/badge.svg)](https://github.com/StefanGrimminck/zgrab2-configurations/actions/workflows/validate-zgrab2-configs.yml)
[![GitHub stars](https://img.shields.io/github/stars/StefanGrimminck/zgrab2-configurations?style=flat)](https://github.com/StefanGrimminck/zgrab2-configurations/stargazers)

Configuration files for [ZGrab2](https://github.com/zmap/zgrab2), the
application-layer scanner from the ZMap project. Each file tells ZGrab2 which
module to run, on which port, and with which options, so you can point a scan at
a specific protocol, product, or exposure without writing the flags by hand.

The ports, endpoints, and CVEs targeted under `service-discovery/` and
`vulnerabilities/` come from live scanning traffic recorded by
[Honeylabs](https://honeylabs.net), a network of internet-facing honeypots. A
config gets added here because real scanners were seen requesting exactly that
port and path, not because it looked interesting on paper.

Every probe follows the ethics note in ZGrab2's own README: it collects only
what any standard client gets without authenticating, and it never exploits a
vulnerability. See [Responsible use](#responsible-use).

## Layout

| Folder | What it holds |
| --- | --- |
| `base-configurations/` | One file per ZGrab2 module, with its options listed as comments. `all.ini` and `all_trigger-on-port.ini` bundle every module into one scan. Copy one of these to write your own config. |
| `service-discovery/` | Fingerprints a specific product on its usual port. |
| `vulnerabilities/misconfigurations/` | Detects a dangerous default, an exposed file or an unauthenticated API. |
| `vulnerabilities/cve/` | Fingerprints a product affected by a specific CVE, and its version where the service publishes one. |
| `tools/` | `lint.py` checks the conventions, `catalog.py` builds the catalog. |

**[CATALOG.md](CATALOG.md) lists every config** with its port, the request it
sends and what it finds, including the CVE table. It is generated from the INI
files, so it is always current.

Every protocol module that upstream ZGrab2 ships has a base file: HTTP, TLS,
JARM, SSH, FTP, SMTP, IMAP, POP3, ManageSieve, Telnet, SMB, MSRPC, MSMQ, RDP,
PPTP, SOCKS5, SNMP, NTP, IPP, MySQL, MSSQL, Postgres, Oracle, MongoDB, Redis,
memcached, IBM DB2 (DRDA), AMQP, MQTT, Check Point, and the industrial
protocols Modbus, DNP3, BACnet, Siemens S7, Fox, EtherNet/IP, CODESYS v2 and
v3, GE SRTP, Omron FINS, PC WorX, ProConOS and Red Lion Crimson.

## Dependencies

- [ZGrab2](https://github.com/zmap/zgrab2) runs the scans.
- [ZMap](https://github.com/zmap/zmap) finds hosts that have a given port open.

## Usage

ZGrab2 reads targets from standard input or `--input-file`, one per line, and
writes one JSON object per target. Each module result carries a `status` field
(`success`, `connection-timeout` and so on) and a `result` object with the
captured data. Each input line has up to four fields, as described in the
[ZGrab2 README](https://github.com/zmap/zgrab2#input-format):

```text
IP, DOMAIN, TAG, PORT
```

Only `IP` or `DOMAIN` is required. With both, ZGrab2 connects to the IP and uses
the domain for the HTTP Host header and TLS SNI. `TAG` selects modules by
trigger (below), and `PORT` overrides the config's port for that line.

Scan a list of hosts with one config:

```bash
cat input.txt | zgrab2 -b blocklist.conf multiple -c service-discovery/ollama.ini -o output.json
```

Find open Elasticsearch instances with ZMap, then check what they expose:

```bash
zmap -p 9200 | zgrab2 -b blocklist.conf multiple -c vulnerabilities/misconfigurations/elasticsearch-indices.ini -o output.json
```

Run every module at once:

```bash
cat input.txt | zgrab2 -b blocklist.conf multiple -c base-configurations/all.ini -o output.json
```

ZGrab2 records responses but does not assert on them. Each config's comment
names the marker that proves a hit, such as a header, a JSON field or a page
title, so filter the output on that marker.

### Port-based triggers

`all_trigger-on-port.ini` sets a `trigger` on every module, equal to its port.
ZGrab2 runs a module only for input lines whose `TAG` matches its trigger, so put
the open port found by ZMap in the tag field:

```text
192.0.2.10, , 22
192.0.2.11, example.com, 443
```

```bash
cat input.txt | zgrab2 -b blocklist.conf multiple -c base-configurations/all_trigger-on-port.ini -o output.json
```

### Blocklist

ZGrab2 exits at startup unless it can read a blocklist: either
`~/.config/zgrab2/blocklist.conf` or the file passed with `-b`. List the
networks you must never scan in it, such as your own infrastructure and any
range you have no permission to test.

## Writing your own config

Copy the matching file from `base-configurations/`, set `name`, `port` and the
options you need, and save it in the folder that fits its purpose. Run
`zgrab2 <module> --help` to confirm option names, which change between ZGrab2
releases. [CONTRIBUTING.md](CONTRIBUTING.md) has the full conventions, including
the rule that a product-named probe must be specific to that product.

## Validation

GitHub Actions runs on every push, every pull request and weekly:

- `tools/lint.py` checks the conventions and refuses requests that exploit a
  vulnerability, such as path traversal, encoded separators, system file reads
  or methods other than GET and HEAD.
- `tools/catalog.py --check` fails when CATALOG.md does not match the configs.
- Upstream ZGrab2 is built from source and loads every INI with
  `zgrab2 multiple` against loopback. A rejected config fails the run, and the
  results are uploaded as a TSV and JSON report.

A config that loads has parsed and initialised; it does not by itself show that
the probe identifies a live service.

## Responsible use

These configs are for authorised security research, asset inventory and
defensive monitoring. They follow the ethics note of
[ZGrab2](https://github.com/zmap/zgrab2#readme):

> ZGrab will only collect information that is available to any standard
> application client _without_ authenticating. We will not accept contributions
> that attempt to gain access to systems by exploiting vulnerabilities or
> attempting to brute-force credentials.

So a CVE config identifies an affected product and its published version; it
never sends the exploit to prove it. The exposure checks under
`vulnerabilities/misconfigurations/` read files and APIs that a server hands to
anyone, which can include secrets such as `.env` files or cloud credentials:
treat the output as sensitive and report what you find to the owner. Only scan
hosts you own or have explicit permission to test, and keep the blocklist
configured.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE). This matches the
license of [ZGrab2](https://github.com/zmap/zgrab2) itself.
