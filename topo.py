from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host
from mininet.node import OVSKernelSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf

def MyNetwork(customTopo):
	net = Mininet(topo=customTopo, build=False, ipBase='10.0.0.0/24', link=TCLink, autoSetMacs=True)
	
	info("***Adding Controller***")

	myController = net.addController(name='localController', 
			controller=RemoteController, ip='127.0.0.1', port=6633)
	for controller in net.controllers:
		controller.start()

	net.build()
	net.start()
	CLI(net)
	net.stop()

class MyTopo(Topo):
	def __init__(self):
		
		# Initialize topology
		Topo.__init__(self)
		
		# Add hosts
		attacker = self.addHost('attacker')
		user = self.addHost('user')
		target = self.addHost('target')
		
		# Add switches
		s1 = self.addSwitch('s1',protocols='OpenFlow13')
		s2 = self.addSwitch('s2',protocols='OpenFlow13')
		s3 = self.addSwitch('s3',protocols='OpenFlow13')

		# Add links for s1
		self.addLink( s1, target)
		self.addLink( s1, s2)
		self.addLink( s1, s3)
		self.addLink( s2, attacker)
		self.addLink( s3, user)


topos = {'mytopo':(lambda: MyTopo())} 

if __name__=='__main__':
	setLogLevel('info')
	MyNetwork(MyTopo())
	
