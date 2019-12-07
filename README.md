# ZGrab 2.0 configuration files
A repository for possible ZGrab 2.0 configurations

## Examples
Default input and output files are specified as `input.txt` and `output.txt`. These should be located in the same directory as zgrab or be changed to your custom settings.

### Scanning all addresses for all supported protocols
``` bash
./zgrab2 multiple -c all.ini
```

### Using port based triggers (as specified [here](https://github.com/zmap/zgrab2#multiple-module-usage)) for scanning

`input.txt` should be structured as follows:
[ip address], [hostname], [port nummer]

e.g. 
``` 
64.233.160.0, google.nl, 23
127.0.0.1, , 22
157.55.33.18, bing.nl, 102
```

``` bash
./zgrab2 multiple -c all_trigger-on-port.ini --trigger
```
