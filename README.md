## st2 ping pack

Sensor based on [fork from sourceperl/th_pinger.py](https://gist.github.com/irom77/794c18ba392e42e944b09c42493b1786)

## Configuration

 * `threads`: 100
 * `targets`: "/opt/stackstorm/static/webui/pinglist.txt"
 * `output`: "ping.txt"
 * `timeout`: 1
 * `count`: 1
 * `url`: "1.1.1.1:8086"
 * `username`: "influxdb"    
 * `password`: "password"  
 * `db`: "influxdb"
 * `quantile`: "0.75"

## Actions

