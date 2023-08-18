# Name: Tomasz Targiel


class ARPSpoofingDetection:
    arp_table = {}

    def detect(self, ip: str, mac: str) -> bool:
        """
        Args:
            ip: ip is at ...
            mac: ... is at mac
        Returns:
            True if something fishy was detected and False otherwise
        """
        arpT = ARPSpoofingDetection.arp_table
        for x, y in arpT.items():
            if (x == ip) and (y != mac): # If some IP response comes from other MAC than the one which was in ARP table
                return True
            if (x != ip) and (y == mac): # If one MAC address represents more than one (previously known) IP address in ARP table
                return True
        arpT.update({ip: mac}) # Add IP and corresponding MAC addresses to ARP table
        return False


if __name__ == "__main__":
    spoofing_detection = ARPSpoofingDetection()

    ip, mac = "134.96.235.129", "a0:36:9f:89:69:5e"  # New entry
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.137", "38:c9:86:3a:48:96"  # New entry
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.142", "98:5a:eb:e4:67:67"  # New entry <- could be the one spoofing, but it's not suspicious yet
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.142", "98:5a:eb:dd:61:4d"  # Now it is clear that someone spoofed
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if check else 'incorrect!'}")

    print()
    spoofing_detection = ARPSpoofingDetection() # "reset" of the network and the switch

    ip, mac = "134.96.235.129", "a0:36:9f:89:69:5e"  # New entry <- not suspicious yet
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.137", "38:c9:86:3a:48:96"  # New entry
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.142", "98:5a:eb:e4:67:67"  # New entry
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if not check else 'incorrect!'}")

    ip, mac = "134.96.235.153", "a0:36:9f:89:69:5e"  # Claims to be two different ip addresses
    check = spoofing_detection.detect(ip, mac)
    print(f"Detection for {ip}/{mac} was {'correct!' if check else 'incorrect!'}")
