from mininet.topo import Topo

class MyProjectTopo(Topo):
    def build(self):
        # Add two hosts and one switch
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')

        # Link them together
        self.addLink(h1, s1)
        self.addLink(h2, s1)

topos = {'project17': (lambda: MyProjectTopo())}
