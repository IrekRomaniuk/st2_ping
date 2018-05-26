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
       

        
    def setup(self):               
        self._timeout=int(self._config['timeout'])
        self._count=int(self._config['count'])  
        self._threads=int(self._config['threads']) # threads: 100
       

    def poll(self):        
        self._logger.debug('########## Pinger dispatching trigger...')   
        # 
        num_threads = self._threads
        ips_q = Queue.Queue()
        out_q = Queue.Queue()
        payload={}
        ips = []
        for i in range(1,255):
            for j in range(192,200): #192,207
                ips.append("10." + str(j) + "." + str(i) + ".1")
        self._logger.debug('########## First: {} Last: {} Number: {}'.format(ips[0],ips[len(ips)-1], len(ips)))
        # start the thread pool
        for i in range(num_threads):
            worker = Thread(target=self.thread_pinger, args=(i, ips_q))
            worker.setDaemon(True)
            worker.start()

        # fill queue
        for ip in ips:
            ips_q.put(ip)

        # wait until worker threads are done to exit
        ips_q.join()

        # print result
        while True:
            try:
                msg = out_q.get_nowait()
            except Queue.Empty:
                break
            self._logger.debug('##########  Result: {}'.format(msg))
            payload['msg']=msg
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
                out_q.put("OK " + str(ip) + " rtt= "+ ping_rtt)

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