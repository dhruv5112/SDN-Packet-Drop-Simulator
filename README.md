PROJECT: PACKET DROP SIMULATOR
1. Problem Statement
In modern network security, the ability to dynamically block malicious or unauthorized traffic at the hardware level is critical. This project demonstrates an SDN-based Packet Drop Simulator. The goal is to create a "Smart Firewall" logic that:

Allows standard communication (ICMP/Ping).

Identifies specific protocols (UDP) in real-time.

Automatically pushes a Drop Rule to the switch to simulate 100% packet loss for that specific flow.

2. System Architecture
The project uses the POX Controller to manage an Open vSwitch (OVS) instance within a Mininet environment.

Control Plane: Custom Python logic (drop_controller.py) using the OpenFlow protocol.

Data Plane: A single switch (s1) and two hosts (h1, h2) connected via a custom topology (topo.py).

3. Implementation Logic
The core logic resides in the _handle_PacketIn function. When the controller sees a packet:

Step 1: It parses the packet to check the IP protocol.

Step 2: If the protocol is UDP (Protocol 17), the controller creates an ofp_flow_mod message.

Step 3: The message contains a match for UDP but an empty action list.

Step 4: In OpenFlow, a match with no action results in the switch dropping the packet.

4. Execution & Verification
Test 1: Connectivity (Ping)
Normal traffic is allowed by the controller to ensure network health.

Command: h1 ping -c 3 h2

Result: 0% packet loss.

Test 2: Packet Drop Simulation (iperf)
UDP traffic is generated to trigger the simulator's drop logic.

Command: h1 iperf -c 10.0.0.2 -u -t 5

Result: 0.00 bits/sec (100% loss).

Test 3: Flow Table Verification
We verify that the rule was installed in the switch hardware.

Command: sh ovs-ofctl dump-flows s1

Result: priority=1,udp,actions= (Empty action confirmed).

5. Conclusion
This simulation successfully demonstrates how SDN can be used for granular traffic control. By offloading the "Drop" action to the switch hardware, we reduce the load on the controller while effectively securing the network against unauthorized UDP traffic.
