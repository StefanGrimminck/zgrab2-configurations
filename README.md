# ZGrab 2.0 configuration files

Configuration files for [ZGrab2](https://github.com/zmap/zgrab2), the
application-layer scanner from the ZMap project. Each file tells ZGrab2 which
module to run, on which port, and with which options, so you can point a scan at
a specific protocol, product, or exposure without writing the flags by hand.

The files under `service-discovery/` and `vulnerabilities/` follow what
internet-facing honeypots actually receive. The ports, endpoints, and CVEs they
target are ones seen in live scanning traffic, not a theoretical list. The
`vulnerabilities/exploitation/` probes are detection-only, covered under
[Responsible use](#responsible-use).

## Dependencies

- [ZGrab2](https://github.com/zmap/zgrab2) runs the scans in this repository.
- [ZMap](https://github.com/zmap/zmap) finds hosts that have a given port open.

## Layout

- `base-configurations/` holds one file per ZGrab2 module, such as `http`,
  `ssh`, `redis`, `mysql`, and `mongodb`. `all.ini` and
  `all_trigger-on-port.ini` bundle every module into one scan. Copy one of these
  when writing your own config.
- `service-discovery/` fingerprints a specific product on its usual port.
- `vulnerabilities/misconfigurations/` detects a dangerous default or an
  exposure, such as a readable `/.git/config` or an open database.
- `vulnerabilities/exploitation/` detects a host that is vulnerable to a
  specific CVE. Each file names its CVE on the first line.

## What is covered

Protocol modules, in `base-configurations/`: HTTP, SSH, FTP, SMTP, IMAP, POP3,
Telnet, TLS, SMB, MySQL, MSSQL, Postgres, MongoDB, Redis, Oracle, NTP, IPP,
Modbus, DNP3, BACnet, Siemens S7, and Fox.

Products and exposures, in `service-discovery/` and `vulnerabilities/`:

- Edge security appliances and VPNs: Fortinet FortiGate, Cisco ASA WebVPN,
  SonicWall, Ivanti Connect Secure, Citrix Gateway, F5 BIG-IP, Palo Alto
  GlobalProtect, Check Point.
- Web platforms and CMS: WordPress, Joomla, Drupal, Magento, Atlassian
  Confluence, GitLab, phpMyAdmin, and Adminer.
- Databases, caches, and search: MongoDB, Redis, Elasticsearch, CouchDB,
  Couchbase, ClickHouse, memcached, InfluxDB, Solr, Neo4j, Riak, Druid.
- Additional data, search, and AI services: CockroachDB, CrateDB, QuestDB,
  YugabyteDB, Meilisearch, Typesense, Qdrant, Milvus,
  Weaviate, Chroma, Marqo, Vespa, and LocalStack.
- Containers, orchestration, and secrets: Docker Engine API, Docker Registry,
  Harbor, Kubernetes API server, kubelet, Portainer, Nomad, etcd, Consul,
  HashiCorp Vault, Argo Workflows, AWX, and Dapr.
- Proxies, storage, and infrastructure management: Caddy, Traefik, Envoy,
  HAProxy, Kong, SeaweedFS, Proxmox VE, OpenStack Keystone, Webmin, Cockpit,
  and pgAdmin.
- CI/CD and developer surfaces: TeamCity, Spring Boot Actuator, Swagger and
  OpenAPI, GraphQL, Symfony, Laravel, GoCD, SonarQube, Nexus Repository, and
  Artifactory.
- Monitoring, dashboards, and messaging: Prometheus, Kibana, Zabbix, Cacti,
  Netdata, Splunk, RabbitMQ, Apache ActiveMQ, NATS,
  Apache ZooKeeper, Alertmanager, Loki, Thanos, VictoriaMetrics, Graylog,
  Sentry, Jaeger, Zipkin, SigNoz, Graphite, Apache Pulsar, Kafka Connect,
  Schema Registry, EMQX, and Apache Artemis.
- Mail, identity, and remote access: Microsoft Exchange, RD Web Access, WinRM,
  Keycloak, Nextcloud and ownCloud.
- Application servers: Oracle WebLogic, GlassFish, Apache Tomcat, Adobe
  ColdFusion, GeoServer, Nacos, Jolokia, WildFly, Hawtio, H2, Apache NiFi,
  Apache Flink, Apache Storm, and Apache OFBiz.
- Identity, collaboration, automation, and web applications: authentik, Dex,
  ZITADEL, Teleport, Ory, Mattermost, n8n, Home Assistant, Rundeck, Directus,
  Strapi, Ghost, MediaWiki, TYPO3, Shopware, Odoo, Umbraco, and Guacamole.
- IoT, routers, and cameras: Hikvision, Axis, Realtek, D-Link, TP-Link, DrayTek,
  Dasan GPON, Boa-based routers, QNAP, Technicolor, Google Home.
- Common exposures: readable Git, Subversion, and Mercurial metadata; `.env`
  variants; AWS, Azure, Google Cloud, Docker, Kubernetes, and Terraform
  credentials; public application configuration and database backups; exposed
  Docker daemons and registries; Spring Actuator `env`, `heapdump`, mappings,
  configuration, log, thread, audit, and session data; Apache `server-status`
  and `server-info`; Go `pprof`; open MongoDB, Redis, memcached, CouchDB and
  Solr; `phpinfo()`; directory traversal to `/etc/passwd`; Hadoop and YARN;
  the Squid cache manager; and unauthenticated Jupyter, kubelet, etcd, Consul,
  Nomad, and Prometheus data APIs.

CVE detection probes currently cover CVE-2012-1823, CVE-2014-8361,
CVE-2015-2051, CVE-2017-9841, CVE-2018-10561, CVE-2018-13379, CVE-2018-20062,
CVE-2019-9082, CVE-2019-17558, CVE-2020-3452, CVE-2020-5902, CVE-2020-8515,
CVE-2020-14882, CVE-2020-25078, CVE-2021-41773, CVE-2021-34473,
CVE-2021-35587, CVE-2021-36260, CVE-2021-43798,
CVE-2023-1389, CVE-2023-20198, and CVE-2024-4577.

## Usage

ZGrab2 reads targets on standard input, one per line, and writes one JSON object
per target to standard output. Each module result carries a `status` field
(`success`, `connection-refused`, and so on) and a `result` object with the
captured data. The examples below use `input.txt` and `output.txt`. Place them
next to the binary or replace them with your own paths.

Scan a list of hosts with every supported protocol:

```bash
cat input.txt | zgrab2 multiple -c base-configurations/all.ini -o output.txt
```

Scan with a single protocol:

```bash
cat input.txt | zgrab2 multiple -c base-configurations/ssh.ini -o output.txt
```

### Continuous validation

The GitHub Actions workflow builds upstream ZGrab2 and loads every INI with
`zgrab2 multiple` on each push and pull request. It targets loopback only,
uploads TSV and JSON reports as workflow artifacts, and fails when any
configuration is rejected. An accepted configuration has parsed and
initialized successfully; it does not by itself identify a live remote service.

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

`all_trigger-on-port.ini` uses ZGrab2's per-module `trigger` field. Its
triggers are port numbers, so put the discovered port in the input CSV's tag
field (the third field). ZGrab2 runs only the module whose trigger matches that
tag. Each input line is `ip, hostname, tag`, where the IP or hostname is
required:

```
64.233.160.0, google.nl, 23
127.0.0.1, , 22
, bing.nl, 102
```

```bash
cat input.txt | zgrab2 multiple -c base-configurations/all_trigger-on-port.ini -o output.txt
```

## Blocklist

Recent ZGrab2 builds will not start without a blocklist file. Pass one with
`-b /path/to/blocklist.conf`, or create the file ZGrab2 names in its startup
error. List the networks you must never scan in it, such as your own
infrastructure and any ranges you do not have permission to touch.

## Writing your own config

Copy the matching file from `base-configurations/`, set `name`, `port`, and any
module options, and save it under the directory that fits its purpose. The
commented options in each base file list what the module accepts. Run
`zgrab2 <module> --help` to confirm the current option names before you rely on
them, since some have changed across ZGrab2 releases. Boolean options must be
written as `option=true` rather than as a bare key.

For a product-named discovery probe, the port and request URI together must be
strongly product-specific. Do not label a generic response from `/`, `/health`,
`/healthz`, `/login`, or a generic API path as a particular product when it
could plausibly be another application. ZGrab2 records the response but does
not enforce body or header assertions from these INI files, so confirm the
expected response marker in the scan output before treating a result as a
fingerprint.

## Responsible use

These configurations are for authorised security research, asset inventory, and
defensive monitoring. The probes under `vulnerabilities/exploitation/` detect a
vulnerable endpoint or read a single known indicator. They do not execute code
or send a working exploit. Only scan hosts that you own or have explicit
permission to test, and keep the blocklist configured so that networks you must
not touch are excluded.
