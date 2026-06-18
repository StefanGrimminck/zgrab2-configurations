# ZGrab 2.0 configuration files

A collection of ready-to-run [ZGrab2](https://github.com/zmap/zgrab2)
configurations for network reconnaissance and exposure research, paired with
[ZMap](https://github.com/zmap/zmap) for host discovery.

The configs under `service-discovery/` and `vulnerabilities/` are informed by
traffic actually observed against internet-facing honeypots: the ports,
endpoints and CVEs here are the ones being probed in the wild right now, not a
theoretical list.

## Dependencies
- ZGrab2 https://github.com/zmap/zgrab2
- ZMap https://github.com/zmap/zmap

## Layout

| Directory | What's in it |
|-----------|--------------|
| `base-configurations/` | One template per ZGrab2 protocol module (`http`, `ssh`, `redis`, `mysql`, `mongodb`, ...), plus `all.ini` and `all_trigger-on-port.ini` that bundle them. Start here to build your own. |
| `service-discovery/` | Fingerprint a specific exposed product: Elasticsearch, Kibana, Docker, Ollama, RabbitMQ, Vault, GlobalProtect, ... |
| `vulnerabilities/misconfigurations/` | Detect dangerous-by-default exposures: a readable `/.git/config` or `/.env`, an open MongoDB, an exposed Squid cache manager, ... |
| `vulnerabilities/exploitation/` | Non-destructive CVE **detection** probes (path traversal, source disclosure, vulnerable-endpoint fingerprinting). Each file names its CVE on the first line. |

## Examples
Default input and output files are specified as `input.txt` and `output.txt`. These should be located in the same directory as zgrab or be changed to your custom settings.

### Scanning all addresses for all supported protocols
``` bash
cat input.txt |  zgrab2 multiple -c all.ini -o output.txt
```

### Scanning using a specific protocol
``` bash
cat input.txt |  zgrab2 multiple -c ssh.ini -o output.txt
```

### Scanning the whole IPv4 space for open Elasticsearch databases
``` bash
zmap -p 9200 | zgrab2 multiple -c vulnerabilities/misconfigurations/elasticsearch-indices.ini -o output.txt
```

### Finding exposed Git repositories (one of the highest-volume campaigns we see)
``` bash
zmap -p 443 | zgrab2 multiple -c vulnerabilities/misconfigurations/git-config-exposure.ini -o output.txt
```

### Finding internet-exposed Ollama LLM servers
``` bash
zmap -p 11434 | zgrab2 multiple -c service-discovery/ollama.ini -o output.txt
```

### Using port based triggers (as specified [here](https://github.com/zmap/zgrab2#multiple-module-usage)) for scanning

`input.txt` should be structured as follows where IP or hostname are manditory:
[IP address], [hostname], [port nummer]

e.g. 
``` 
64.233.160.0, google.nl, 23
127.0.0.1, , 22
, bing.nl, 102
```

``` bash
cat input.txt | zgrab2 multiple -c base-configurations/all_trigger-on-port.ini -o output.txt --trigger
```

## Responsible use
These configurations are for authorised security research, asset inventory and
defensive monitoring. The `exploitation/` probes are **detection-only**: they
fingerprint a vulnerable endpoint or read a single known indicator, and never
execute code or send a weaponised payload. Only scan hosts you own or are
explicitly permitted to test, and keep ZGrab2's blocklist configured to exclude
networks you must not touch.
