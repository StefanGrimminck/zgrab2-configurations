# ZGrab 2.0 configuration files

Configuration files for [ZGrab2](https://github.com/zmap/zgrab2), the
application-layer scanner from the ZMap project. Each file tells ZGrab2 which
module to run, on which port, and with which options. This lets you point a
scan at a specific protocol, product, or exposure without writing the flags by
hand.

The files under `service-discovery/` and `vulnerabilities/` follow what
internet-facing honeypots actually receive. The ports, endpoints, and CVEs they
target are ones seen in live scanning traffic, not a theoretical list.

## Dependencies

- [ZGrab2](https://github.com/zmap/zgrab2) runs the scans in this repository.
- [ZMap](https://github.com/zmap/zmap) finds hosts that have a given port open.

## Layout

- `base-configurations/` holds one file per ZGrab2 module, such as `http`,
  `ssh`, `redis`, `mysql`, and `mongodb`. `all.ini` and
  `all_trigger-on-port.ini` bundle every module into one scan. Copy one of
  these when writing your own config.
- `service-discovery/` fingerprints a specific product on its usual port, such
  as Elasticsearch, Docker, Ollama, RabbitMQ, or HashiCorp Vault.
- `vulnerabilities/misconfigurations/` detects a dangerous default or an
  exposure, such as a readable `/.git/config`, an open MongoDB, or an exposed
  Docker daemon.
- `vulnerabilities/exploitation/` detects a host that is vulnerable to a
  specific CVE. Each file names its CVE on the first line. These probes only
  fingerprint the endpoint or read a known indicator. They do not run commands
  or send a working exploit.

## Usage

ZGrab2 reads targets on standard input, one per line, and writes JSON results
to standard output. The examples below use `input.txt` and `output.txt`. Place
them next to the binary or replace them with your own paths.

Scan a list of hosts with every supported protocol:

```bash
cat input.txt | zgrab2 multiple -c base-configurations/all.ini -o output.txt
```

Scan with a single protocol:

```bash
cat input.txt | zgrab2 multiple -c base-configurations/ssh.ini -o output.txt
```

Find open Elasticsearch instances with ZMap, then scan them:

```bash
zmap -p 9200 | zgrab2 multiple -c vulnerabilities/misconfigurations/elasticsearch-indices.ini -o output.txt
```

Find exposed Git repositories:

```bash
zmap -p 443 | zgrab2 multiple -c vulnerabilities/misconfigurations/git-config-exposure.ini -o output.txt
```

Find exposed Ollama servers:

```bash
zmap -p 11434 | zgrab2 multiple -c service-discovery/ollama.ini -o output.txt
```

### Port-based triggers

To run a module only against hosts where a matching port is supplied, use the
trigger form from the
[ZGrab2 multiple-module documentation](https://github.com/zmap/zgrab2#multiple-module-usage).
Each input line is `ip, hostname, port`, where the IP or the hostname is
required:

```
64.233.160.0, google.nl, 23
127.0.0.1, , 22
, bing.nl, 102
```

```bash
cat input.txt | zgrab2 multiple -c base-configurations/all_trigger-on-port.ini -o output.txt --trigger
```

## Writing your own config

Copy the matching file from `base-configurations/`, set `name`, `port`, and any
module options, and save it under the directory that fits its purpose. The
commented options in each base file list what the module accepts. Run
`zgrab2 <module> --help` to confirm the current option names before you rely on
them.

## Responsible use

These configurations are for authorised security research, asset inventory, and
defensive monitoring. The probes under `vulnerabilities/exploitation/` detect a
vulnerable endpoint or read a single known indicator. They do not execute code
or send a working exploit. Only scan hosts that you own or have explicit
permission to test, and keep the ZGrab2 blocklist configured so that networks
you must not touch are excluded.
