from influxdb import InfluxDBClient
import ast
from st2actions.runners.pythonrunner import Action
import padas as pd

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
       
    def run(self, rtt, total): #, tags
        """
        Example of payload
        """
        _db = self.config['db']
        _user = self.config['username']
        _pass = self.config['password']
        _url, _port = self.config['url'].split(":")
        client = InfluxDBClient(_url, _port, _user, _pass, _db)
        # print(_db,_user,_pass,_url, _port)
        # print(ast.literal_eval(rtt))
        rtt = ast.literal_eval(rtt)
        for delay in rtt:        
            #points={}
        result=client.write_points()
        client.close()       
        return result
