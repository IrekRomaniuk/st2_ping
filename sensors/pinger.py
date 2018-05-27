from st2reactor.sensor.base import PollingSensor
from threading import Thread
import subprocess
import Queue
import re
import os

class Pinger(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            get_logger() for writing to logs.
            dispatch() for dispatching triggers into the system.
    * self._config
        - contains configuration that was specified as
          config.yaml in the pack.
    * self._poll_interval
        - indicates the interval between two successive poll() calls.
    """
    def __init__(self, sensor_service, config, poll_interval): #sensor_service, config, poll_interval, 
        super(Pinger, self).__init__(sensor_service=sensor_service,  
                                          config=config,                                 
                                          poll_interval=poll_interval)
        self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
        self.ips = []
        
       
        
    def setup(self):               
        self._timeout=int(self._config['timeout'])
        self._count=int(self._config['count'])  
        self._threads=int(self._config['threads']) # threads: 100
        self._targets=self._config['targets']
        self.ips_q = Queue.Queue()
        self.out_q = Queue.Queue()
        try:
            with open(self._targets, 'r') as f:
                self.ips = f.readlines()
        except IOError: 
            self._logger.debug('########## Can not read file with targets: {}'.format(self._targets))
       

    def poll(self):        
        self._logger.debug('########## Pinger dispatching trigger...')   
        # 
        num_threads = self._threads
        
        payload={}
        payload['msg']=[]
        
        if self.ips:               
            self._logger.debug('########## First: {} Last: {} Number: {}'.format(self.ips[0],self.ips[len(self.ips)-1], len(self.ips)))
        else:
            payload['Error'] = "Can not read file with targets"
            self.sensor_service.dispatch(trigger="ping.pinger", payload=payload)
            return
        # start the thread pool
        for i in range(num_threads):
            worker = Thread(target=self.thread_pinger, args=(i, self.ips_q))
            worker.setDaemon(True)
            worker.start()

        # fill queue
        for ip in self.ips:
            self.ips_q.put(ip)

        # wait until worker threads are done to exit
        self.ips_q.join()

        # print result
        while True:
            try:
                msg = self.out_q.get_nowait()
            except Queue.Empty:
                break
            self._logger.debug('##########  Result: {}'.format(msg))
            payload['msg'].append(msg)
        
        # self._logger.debug('########## Pinger dispatching payload...')
        payload['total']=len(payload['msg'])
        self.sensor_service.dispatch(trigger="ping.pinger", payload=payload) 

    def thread_pinger(self, i, q):
        """Pings hosts in queue"""
        while True:
            # get an IP item form queue
            ip = q.get()
            # ping it
            args=['/bin/ping', '-c', '1', '-W', '1', str(ip)]
            p_ping = subprocess.Popen(args,
                                    shell=False,
                                    stdout=subprocess.PIPE)
            # save ping stdout
            p_ping_out = p_ping.communicate()[0]

            if (p_ping.wait() == 0):
                # rtt min/avg/max/mdev = 22.293/22.293/22.293/0.000 ms
                search = re.search(r'rtt min/avg/max/mdev = (.*)/(.*)/(.*)/(.*) ms', p_ping_out, re.M|re.I)
                ping_rtt = search.group(2)
                self.out_q.put("OK " + str(ip) + " rtt= "+ ping_rtt)

            # update queue : this ip is processed
            q.task_done()

    def cleanup(self):
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass