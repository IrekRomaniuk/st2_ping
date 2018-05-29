## st2 ping pack

Ping pack collecting ping responses from multiple targets (IP addresses) using threads. Includes sensor based on [fork from sourceperl/th_pinger.py](https://gist.github.com/irom77/794c18ba392e42e944b09c42493b1786)

## Configuration

 * `threads`: number of threads i.e. 50 
 * `targets`: location of tragtes (list of IP addresses , oneper line).Recommended is "/opt/stackstorm/static/webui/pinglist.txt" in order to be accessible with https://st2/pinglits.txt
 * `output`: "ping.txt"
 * `timeout`: 1
 * `count`: 1
 * `url`: "1.1.1.1:8086"
 * `username`: "influxdb"    
 * `password`: "password"  
 * `db`: "influxdb"
 * `quantile`: "0.75"

## Actions

