from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ipv4 import ipv4
from pox.lib.packet.udp import udp

log = core.getLogger()

class PacketDropSimulator(object):
    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed: return

        ip_pkt = packet.find('ipv4')
        
        # LOGIC: Identify UDP packets (Protocol 17)
        if ip_pkt and ip_pkt.protocol == ipv4.UDP_PROTOCOL:
            log.info("UDP Detected from %s: Installing DROP rule" % ip_pkt.srcip)
            
            # Create the Flow Mod message
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 20
            # No actions added = DROP
            self.connection.send(msg)
            return

        # BASIC FORWARDING (Learning Switch behavior)
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

def launch():
    def start_switch(event):
        PacketDropSimulator(event.connection)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
