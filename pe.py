"""Class representing a PE router participating in an EVPN"""
import logging
from typing import Dict
from mac_vrf import MAC_VRF


class PE:
    """PE class"""

    def __init__(self, name: str, as_number: int, router_id: str = None):
        self.name = name
        self.as_number = as_number
        self.router_id = router_id
        self.mac_vrfs: Dict[int, MAC_VRF] = {}
        self.last_allocated_rd = 0
        self.logger = None
        self.__create_logger()
        self.logger.info("PE created")

    def __create_logger(self):
        self.logger = logging.getLogger(__name__ + "-" + self.name)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter("%(created)f:%(levelname)s:%(name)s:%(message)s")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def create_service(self, service_id):
        """Creates an instance of a MAC_VRF with given id"""
        self.mac_vrfs[service_id] = MAC_VRF(service_id, self)

    def add_segments_to_service(self, service_id: int, segments: dict):
        """Add segments to a given service"""
        for segment, interface in segments.items():
            self.mac_vrfs[service_id].add_interface(interface, segment)

    def get_new_rd(self):
        """Return unique Route Distinguisher for this PE"""
        self.last_allocated_rd += 1
        return self.name + ":" + str(self.last_allocated_rd)
