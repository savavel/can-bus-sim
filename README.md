# can-bus-sim

The project is part of a Fog Network Simulator which tries to simulate the use case of a vehicle collision on a public road and prevent further incidents by sending alerts to other drivers in the vicinity.


CAN (Controller Area Network) Bus simulator used for mimicking an internal vehicle network.

It uses keyboard press inputs to send signals on the CAN Bus which can be processed by any device connected on the bus.

The HEX codes used in the simulation are example ones and can be modified.

The Simulator includes an SSL socket forwarder which forwards the packets over a traditional TCP connection to achive authentication.
