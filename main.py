"""Main Program"""

from dataclasses import dataclass
from typing import Dict, List
from pe import PE


@dataclass
class EVPNSpec:
    """
    Dataclass Representing an EVPN instance
    pes is of format: {PE name: {ESI:interface}}
    """

    vlan_id: int
    service_id: int
    pes: Dict[str, Dict[int, str]]


def main():

    """
    Create a point to point EVPN between 2 PEs
     - VLAN ID = 5
     - Service ID = 1985
     - PE1 connected to ESI 1 via interface 1/1:5
     - PE2 connected to ESI 2 via interface 1/1:5
    """
    evpn1 = EVPNSpec(
        vlan_id=5,
        service_id=1985,
        pes={"PE1": {1: "1/1:5"}, "PE2": {2: "1/1:5"}},
    )

    pes: List[PE] = []
    as_number = 1951
    for pe_name, segments in evpn1.pes.items():
        new_pe = PE(pe_name, as_number)
        new_pe.create_service(evpn1.service_id)
        new_pe.add_segments_to_service(evpn1.service_id, segments)
        pes.append(new_pe)

    pes[0].mac_vrfs[evpn1.service_id].update_mac_table("New_MAC_1", "1/1:5")
    pes[1].mac_vrfs[evpn1.service_id].update_mac_table("New_MAC_2", "1/1:5")

    pass


if __name__ == "__main__":
    main()
