# ZGrab2 configurations

*Honeypot-informed scan configs for [ZGrab2](https://github.com/zmap/zgrab2): service discovery, misconfiguration checks, and CVE detection.*

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
port and path, not because it looked interesting on paper. The
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
  YugabyteDB, Meilisearch, Typesense, Qdrant, Milvus, Weaviate, Chroma, Marqo,
  Vespa, LocalStack, Ollama, and ComfyUI.
- Containers, orchestration, and secrets: Docker Engine API, Docker Registry,
  Harbor, Kubernetes API server, kubelet, Portainer, Nomad, etcd, Consul,
  HashiCorp Vault, Argo Workflows, AWX, and Dapr.
- Proxies, storage, and infrastructure management: Caddy, Traefik, Envoy,
  HAProxy, Kong, SeaweedFS, MinIO, Proxmox VE, VMware vCenter, OpenStack
  Keystone, Webmin, Cockpit, and pgAdmin.
- CI/CD and developer surfaces: TeamCity, Spring Boot Actuator, Swagger and
  OpenAPI, GraphQL, Symfony, Laravel, GoCD, SonarQube, Nexus Repository, and
  Artifactory.
- Monitoring, dashboards, and messaging: Prometheus, Kibana, Metabase, Zabbix,
  Cacti, Checkmk, OpenNMS, Kiali, Netdata, Splunk, RabbitMQ, Apache ActiveMQ, NATS,
  Apache ZooKeeper, Alertmanager, Loki, Thanos, VictoriaMetrics, Graylog,
  Sentry, Jaeger, Zipkin, SigNoz, Graphite, Apache Pulsar, Kafka Connect,
  Schema Registry, EMQX, and Apache Artemis.
- Mail, identity, and remote access: Microsoft Exchange, RD Web Access, WinRM,
  VNC, ScreenConnect, WSUS, MOVEit Transfer, Keycloak, Nextcloud and ownCloud.
- Application servers: Oracle WebLogic, GlassFish, Apache Tomcat, Adobe
  ColdFusion, GeoServer, Nacos, Jolokia, WildFly, Hawtio, H2, Apache NiFi,
  Apache Flink, Apache Storm, Apache OFBiz, and SAP NetWeaver.
- Identity, collaboration, automation, and web applications: authentik, Dex,
  ZITADEL, Teleport, Ory Hydra, Ory Kratos, Mattermost, n8n, Kestra, Home
  Assistant, Homebridge, Immich, Rundeck, Directus, Strapi, Ghost, MediaWiki,
  TYPO3, Shopware, Odoo, Umbraco, and Guacamole.
- IoT, routers, cameras, and industrial control: Hikvision, Axis, Realtek,
  D-Link, TP-Link, DrayTek, Dasan GPON, Boa-based routers, QNAP, Technicolor,
  Google Home, and Red Lion HMI panels.
- Healthcare imaging: dcm4chee-arc, an open-source DICOM/PACS archive.
- Common exposures: readable Git, Subversion, and Mercurial metadata; `.env`
  variants; AWS, Azure, Google Cloud, Docker, Kubernetes, and Terraform
  credentials; public application configuration and database backups; exposed
  Docker daemons and registries; Spring Actuator `env`, `heapdump`, mappings,
  configuration, log, thread, audit, and session data; Apache `server-status`
  and `server-info`; Go `pprof`; open MongoDB, Redis, memcached, CouchDB and
  Solr; `phpinfo()`; directory traversal to `/etc/passwd`; a public
  `Jenkinsfile`; Hadoop and YARN; the Squid cache manager; and unauthenticated
  Jupyter, kubelet, etcd, Consul, Nomad, and Prometheus data APIs.

### CVE detection probes

Each row is a config under `vulnerabilities/exploitation/` that fingerprints a
specific CVE without executing an exploit.

| CVE | Product | Config |
| --- | --- | --- |
| CVE-2014-8361 | Realtek SDK "miniigd" UPnP (multiple OEM routers) | [`realtek-miniigd-CVE-2014-8361.ini`](vulnerabilities/exploitation/realtek-miniigd-CVE-2014-8361.ini) |
| CVE-2015-2051 | D-Link HNAP | [`dlink-hnap-CVE-2015-2051.ini`](vulnerabilities/exploitation/dlink-hnap-CVE-2015-2051.ini) |
| CVE-2017-9841 | PHPUnit `eval-stdin.php` | [`phpunit-CVE-2017-9841.ini`](vulnerabilities/exploitation/phpunit-CVE-2017-9841.ini) |
| CVE-2018-10561 | Dasan GPON home routers | [`dasan-gpon-CVE-2018-10561.ini`](vulnerabilities/exploitation/dasan-gpon-CVE-2018-10561.ini) |
| CVE-2018-13379 | Fortinet FortiOS SSL VPN | [`fortios-CVE-2018-13379.ini`](vulnerabilities/exploitation/fortios-CVE-2018-13379.ini) |
| CVE-2018-20062 | ThinkPHP `invokefunction` (also CVE-2019-9082) | [`thinkphp-CVE-2018-20062.ini`](vulnerabilities/exploitation/thinkphp-CVE-2018-20062.ini) |
| CVE-2019-11510 | Pulse Connect Secure / Ivanti Connect Secure SSL VPN | [`pulse-secure-CVE-2019-11510.ini`](vulnerabilities/exploitation/pulse-secure-CVE-2019-11510.ini) |
| CVE-2019-19781 | Citrix ADC / Citrix Gateway | [`citrix-adc-CVE-2019-19781.ini`](vulnerabilities/exploitation/citrix-adc-CVE-2019-19781.ini) |
| CVE-2020-3452 | Cisco ASA / Firepower Threat Defense | [`cisco-asa-CVE-2020-3452.ini`](vulnerabilities/exploitation/cisco-asa-CVE-2020-3452.ini) |
| CVE-2020-5902 | F5 BIG-IP TMUI | [`f5-big-ip-CVE-2020-5902.ini`](vulnerabilities/exploitation/f5-big-ip-CVE-2020-5902.ini) |
| CVE-2020-8515 | DrayTek Vigor routers | [`draytek-vigor-CVE-2020-8515.ini`](vulnerabilities/exploitation/draytek-vigor-CVE-2020-8515.ini) |
| CVE-2020-14882 | Oracle WebLogic console | [`oracle-weblogic-CVE-2020-14882.ini`](vulnerabilities/exploitation/oracle-weblogic-CVE-2020-14882.ini) |
| CVE-2020-25078 | D-Link DCS-2530L / DCS-2670L cameras | [`dlink-dcs-CVE-2020-25078.ini`](vulnerabilities/exploitation/dlink-dcs-CVE-2020-25078.ini) |
| CVE-2021-26084 | Confluence Server / Data Center (Webwork OGNL injection) | [`confluence-CVE-2021-26084.ini`](vulnerabilities/exploitation/confluence-CVE-2021-26084.ini) |
| CVE-2021-34473 | Microsoft Exchange (ProxyShell) | [`exchange-proxyshell-CVE-2021-34473.ini`](vulnerabilities/exploitation/exchange-proxyshell-CVE-2021-34473.ini) |
| CVE-2021-35587 | Oracle Access Manager (Fusion Middleware) | [`oracle-fusion-middleware-CVE-2021-35587.ini`](vulnerabilities/exploitation/oracle-fusion-middleware-CVE-2021-35587.ini) |
| CVE-2021-36260 | Hikvision camera / NVR | [`hikvision-CVE-2021-36260.ini`](vulnerabilities/exploitation/hikvision-CVE-2021-36260.ini) |
| CVE-2021-41773 | Apache HTTP Server | [`apache-httpd-CVE-2021-41773.ini`](vulnerabilities/exploitation/apache-httpd-CVE-2021-41773.ini) |
| CVE-2021-43798 | Grafana | [`grafana-CVE-2021-43798.ini`](vulnerabilities/exploitation/grafana-CVE-2021-43798.ini) |
| CVE-2023-1389 | TP-Link Archer AX21 | [`tp-link-CVE-2023-1389.ini`](vulnerabilities/exploitation/tp-link-CVE-2023-1389.ini) |
| CVE-2023-20198 | Cisco IOS XE Web UI | [`cisco-ios-xe-CVE-2023-20198.ini`](vulnerabilities/exploitation/cisco-ios-xe-CVE-2023-20198.ini) |
| CVE-2023-38646 | Metabase (pre-auth setup-token) | [`metabase-CVE-2023-38646.ini`](vulnerabilities/exploitation/metabase-CVE-2023-38646.ini) |
| CVE-2023-49103 | ownCloud graphapi (phpinfo disclosure) | [`owncloud-CVE-2023-49103.ini`](vulnerabilities/exploitation/owncloud-CVE-2023-49103.ini) |
| CVE-2024-1709 | ConnectWise ScreenConnect | [`screenconnect-CVE-2024-1709.ini`](vulnerabilities/exploitation/screenconnect-CVE-2024-1709.ini) |
| CVE-2024-4577 | PHP-CGI on Windows (revives CVE-2012-1823) | [`php-cgi-CVE-2024-4577.ini`](vulnerabilities/exploitation/php-cgi-CVE-2024-4577.ini) |
| CVE-2025-31324 | SAP NetWeaver Visual Composer | [`sap-netweaver-CVE-2025-31324.ini`](vulnerabilities/exploitation/sap-netweaver-CVE-2025-31324.ini) |

`vulnerabilities/misconfigurations/solr-admin.ini` also targets the entry
point for CVE-2019-17558, an unauthenticated Solr admin exposure rather than a
single CVE-specific request.

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
