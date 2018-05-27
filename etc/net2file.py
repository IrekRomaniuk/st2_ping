import ipaddress

ips = []
my_net=ipaddress.ip_network(u'10.29.0.0/21') #10.220.192.192/29
for host in my_net.hosts():
  #if (str(host).split('.')[3]) == '1':
    #print(host)
  ips.append(str(host))

print('First: {} Last: {}'.format(ips[0],ips[len(ips)-1]))
print('Numbers of address to ping {}'.format(len(ips)))  


with open("/opt/stackstorm/static/webui/pinglist.txt",'w') as f:
  f.write('\n'.join(ips))
