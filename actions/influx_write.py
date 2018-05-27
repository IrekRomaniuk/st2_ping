from influxdb import InfluxDBClient
import ast
from st2actions.runners.pythonrunner import Action
import pandas as pd

json_rtt = [
    {
        "measurement": "rtt", #pingcount
        "tags": {
            "site": "DC2",           
        },
        "fields": {
            "rtt": 0.411 #total-up
        }
    }
]      

class influx_write(Action):
       
    def run(self, ips, total): #, tags
        """
        Example of payload
        """
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _url, _port = self.config['url'].split(":")
        client = InfluxDBClient(_url, _port, _user, _pass, _db)
        # print(_db,_user,_pass,_url, _port)
        # print(ast.literal_eval(ips))
        ips = ast.literal_eval(ips)
        delay = pd.Series([float(ip.split(':')[1]) for ip in ips]) 
        rtt = delay.quantile(0.75)
        print(rtt)
        result=client.write_points(
            [
                {
                    "measurement": "rtt", 
                    "tags": {
                        "site": "DC2",           
                    },
                    "fields": {
                        "quantile": rtt
                    }
                }
            ]      
        )
        client.close()       
        return result
