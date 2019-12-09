# ZGrab 2.0 configuration files
A repository for possible ZGrab 2.0 configurations

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
zmap -p 9200 | zgrab2 multiple -c custom-services/elasticsearch-indices.ini -o output.txt
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
cat input.txt | zgrab2 multiple -c all_trigger-on-port.ini -o output.txt --trigger
```
