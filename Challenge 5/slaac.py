# Name: Tomasz Targiel


def convert(mac: str, prefix: str) -> str:
    """
    Args:
        mac: You know this one
        prefix: network prefix (64 bit) with ":" at the end
    Returns:
        IPv6 address
    """
    # Split MAC address into octets
    mac_octets = mac.split(':')

    # Convert first octet to binary
    first_octet = bin(int(mac_octets[0], 16))[2:].zfill(8)

    # Flip 7th bit
    if first_octet[6] == "1":
        first_octet = first_octet[:6] + "0" + first_octet[7:]
    else:
        first_octet = first_octet[:6] + "1" + first_octet[7:]

    # Convert back 1st octet to hexadecimal
    mac_octets[0] = hex(int(first_octet, 2))[2:].zfill(2)

    # Insert "ff" and "fe" to mac_octets
    mac_octets.insert(3, "ff")
    mac_octets.insert(4, "fe")

    # Create a new list to hold the joined octets
    joined_octets = []
    # Loop through the octets in pairs
    for i in range(0, len(mac_octets), 2):
        # Join the current pair of octets and then add it to joined_octets list
        joined_octet = ''.join(mac_octets[i:i+2])
        joined_octets.append(joined_octet)

    # Return full IPv6 address
    return prefix + ':'.join(joined_octets)


if __name__ == "__main__":
    mac = "00:0c:f1:8e:c1:d8"
    prefix = "fe80:0000:0000:0000:"

    expected_address = "fe80:0000:0000:0000:020c:f1ff:fe8e:c1d8"
    result_address = convert(mac, prefix)
    print(f"convert({mac, prefix}) = {result_address} and should be {expected_address}, so it {'worked!' if result_address == expected_address else 'did not work!'}")
