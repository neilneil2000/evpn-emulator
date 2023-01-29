"""Class representing a MAC VRF for an EVPN"""

import logging


class MAC_VRF:
    def __init__(self, service_id: int, parent_pe):
        self.id = service_id
        self.parent_pe = parent_pe
        self.route_distinguisher = parent_pe.get_new_rd()
        self.segments = {}
        self.mac_table = {}
        self.advertised_routes = {1: [], 2: [], 3: [], 4: []}
        self.fib = None
        self.stats = None
        self.logger = None
        self.__create_logger()
        self.logger.info("MAC_VRF created")

    def __create_logger(self):
        self.logger = logging.getLogger(
            __name__ + "-" + str(self.id) + "-" + self.parent_pe.name
        )
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(created)f:%(levelname)s:%(name)s:%(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def add_interface(self, interface: str, esi: int):
        """Add a new Ethernet Segment to the VRF"""
        if self.segments.get(esi) is not None:
            raise IndexError("Segment already exists")
        self.logger.info("New Interface Found: ESI=%s Interface=%s", esi, interface)
        self.segments[esi] = interface
        self.__advertise_segment(esi)

    def __advertise_segment(self, esi):
        ethernet_segment_routes = self.advertised_routes[4]
        if esi in ethernet_segment_routes:
            return
        self.logger.info(
            "Advertising Type4 EVPN Route (Ethernet Segment) Segment=%s", esi
        )
        ethernet_segment_routes.append(esi)

    def get_segment_for_interface(self, interface: str):
        """Returns ESI ID of segment related to given interface"""
        for segment, segment_interface in self.segments.items():
            if interface == segment_interface:
                return segment
        raise IndexError("Interface not found on any segment")

    def update_mac_table(self, mac_address: str, interface: str):
        """Update the MAC table and handle control plane signalling to other PEs"""
        self.mac_table[mac_address] = self.get_segment_for_interface(interface)
        self.logger.debug(
            "MAC Address Location Discovered: MAC=%s Interface=%s",
            mac_address,
            interface,
        )
        self.__advertise_mac(mac_address)

    def __advertise_mac(self, mac_address):
        self.logger.debug(
            "Advertising Type2 EVPN Route (MAC Address) MAC ADDRESS=%s SEGMENT=%s",
            mac_address,
            self.mac_table[mac_address],
        )
        self.advertised_routes[2].append(mac_address)

    # BELOW HERE IS STUFF FOR FUTURE UPDATES

    def drop_packet(self, packet, interface):
        """Drop packet received on interface and update stats"""

    def receive_local_packet(self, packet, interface):
        """Process a packet received on a given interface"""
        if interface not in self.interfaces:
            self.drop_packet(packet, interface)
        if packet.src_mac_address not in self.mac_table:
            self.update_mac_table(packet.src_mac_address, interface)
        if packet.dst_mac_address in self.mac_table:
            return self.forward_remote_known(packet)
        self.forward_remote_unknown(packet)

    def forward_remote_known(self, packet):
        """Forward a packet with known destination MAC to remote PE"""

    def forward_remote_unknown(self, packet):
        """Forward a packet with unknown destination MAC to remote PEs"""

    def receive_remote_packet(self, packet):
        """Process a packet received via MPLS backhaul"""
        if self.get_interface(packet.dst_mac_address) is not None:
            return self.forward_local_known
        return self.forward_local_unknown

    def get_interface(self, mac_address):
        """Returns interface that mac_address exists on, or None if unknown"""
        return self.mac_table.get(mac_address)

    def forward_local_known(self, packet):
        """Send packet out of local interface"""
        # Build ethernet frame
        frame = self.build_frame
        interface = self.get_interface
        self.send_frame(frame, interface)

    def send_frame(self, frame, interface):
        """Emulate sending a frame - log that it has been sent"""
