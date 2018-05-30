## Ping pack

*Ping* pack collecting ping responses from multiple targets (IP addresses) using threads. Includes sensor based on [fork from sourceperl/th_pinger.py](https://gist.github.com/irom77/794c18ba392e42e944b09c42493b1786)

## Configuration

 * `threads`: number of threads i.e. 50 
 * `targets`: location of tragtes (list of IP addresses, one per line). Recommended is "/opt/stackstorm/static/webui/pinglist.txt" in order to be accessible with https://st2/pinglits.txt
 * `output`: location of report file i.e. "ping.txt"
 * `timeout`: ping timeout i.e. 1 for 1s
 * `count`: ping count i.e. 1
 * `url`: Influxdb address and port i.e. "1.1.1.1:8086"
 * `username`: Influxdb user i.e. "influxdb"    
 * `password`: Influxdb password i.e. "password"  
 * `db`: Influxdb database name i.e. "influxdb"
 * `quantile`: Pecrent of ping response to report on i.e. "0.75" (cut off outliers)

## Actions

* `influx_write`: Writing average ping delay to Influxdb
* `portal_report`: Reporting average delay per target at https://st2/ping.txt where *ping.txt*S is specified in the config *output*

## Sensor:

* `Pinger`: emitting *pinger* trigger 


