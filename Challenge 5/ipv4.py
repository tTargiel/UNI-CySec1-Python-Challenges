# Name: Tomasz Targiel

import struct


def get_bits(num, start, end, length=8):
    """Like bits(num)[from:to] with length=number_of_bits"""
    mask = 2 ** (end - start) - 1
    shift = length - (end - start) - start
    return (num & (mask << shift)) >> shift


def parseIPv4Header(header: bytes) -> tuple[list[int, int, int, int, int, int, int, int, int, int, int, int, int, bytes], bytes]:
    """
    Parses an IPv4 header.
    Args:
        header: IPv4 header
    Returns:
        ([version, header_length, type_of_service, total_length, identification, flag_mf, flag_df, fragment_offset,
            ttl, proto, checksum, source_addr, dest_addr, options_and_padding], payload)
    """
    # Unpack the header
    (version_and_header_length, type_of_service, total_length, identification, flags_and_fragment_offset,
     ttl, proto, checksum, source_addr, dest_addr) = struct.unpack("!BBHHHBBHII", header[:20])
    # !: Network (big-endian) byte order
    # B: Unsigned char (1 byte)
    # H: Unsigned short (2 bytes)
    # I: Unsigned int (4 bytes)

    # Get the version and header length from the first byte
    version = get_bits(version_and_header_length, 0, 4, 8)
    header_length = get_bits(version_and_header_length, 4, 8, 8)
    header_length_in_bytes = header_length * 4

    # Get the flags from the next two bytes
    flag_df = get_bits(flags_and_fragment_offset, 1, 2, 16)
    flag_mf = get_bits(flags_and_fragment_offset, 2, 3, 16)
    fragment_offset = get_bits(flags_and_fragment_offset, 3, 16, 16)

    # Get the options and padding from the end of the header
    options_and_padding = header[20:header_length_in_bytes]

    # Get the payload from the rest of the packet
    payload = header[header_length_in_bytes:]

    # Return the fields as a list, along with the payload
    return ([version, header_length, type_of_service, total_length, identification, flag_mf, flag_df, fragment_offset,
             ttl, proto, checksum, source_addr, dest_addr, options_and_padding], payload)


def reassembleFragments(fragments: list[bytes]) -> bytes:
    """
    Reassembles IPv4 payload from fragments.
    Args:
        fragments: list of fragments
    Returns:
        assembled payload
    """
    # Store the fragments in a dictionary, with the fragment offset as the key
    fragment_dict = {}
    for fragment in fragments:
        # Parse the IPv4 header to get the fragment offset and MF flag
        (_, _, _, _, _, _, _, fragment_offset, _, _, _, _, _, _), payload = parseIPv4Header(fragment)
        fragment_dict[fragment_offset] = payload

    # Initialize an empty list to store the reassembled fragments
    reassembled_fragments = []

    # Sort the fragments by fragment offset
    sorted_fragments = sorted(fragment_dict.items())

    # Iterate through the sorted fragments and append them to the list of reassembled fragments
    for fragment_offset, fragment in sorted_fragments:
        reassembled_fragments.append(fragment)

    # Concatenate the reassembled fragments to get the final payload
    assembled_payload = b''.join(reassembled_fragments)

    return assembled_payload


if __name__ == "__main__":
    # Test parseIPv4Header
    header = b'F\x00\x00 \x00* \x00\x80\x11\x08\x9e\x7f\x00\x00\x01\x01\x01\x01\x01\x03\x03\x10\x00~\xe0\x00P\x00(\n\x05'

    expected_tuple = ([4, 6, 0, 32, 42, 1, 0, 0, 128, 17, 2206, 2130706433, 16843009, b'\x03\x03\x10\x00'], b'~\xe0\x00P\x00(\n\x05')
    result_tuple = parseIPv4Header(header)

    print(f"Header:             {header}")
    print(f"Resulting tuple:    {result_tuple}")
    print(f"Expected tuple:     {expected_tuple}")
    print(f"Worked:             {expected_tuple == result_tuple}")
    print()

    # Test reassembleFragments
    fragments = [
        b'F\x00\x00 \x00* \x00\x80\x11\x08\x9e\x7f\x00\x00\x01\x7f\x00\x00\x01\x03\x03\x10\x00~\xe0\x00P\x00(\n\x05',
        b'F\x00\x00 \x00* \x02\x80\x11\x08\x9c\x7f\x00\x00\x01\x7f\x00\x00\x01\x03\x03\x10\x00cheap. S',
        b'F\x00\x00 \x00* \x01\x80\x11\x08\x9d\x7f\x00\x00\x01\x7f\x00\x00\x01\x03\x03\x10\x00Talk is ',
        b'F\x00\x00 \x00* \x03\x80\x11\x08\x9b\x7f\x00\x00\x01\x7f\x00\x00\x01\x03\x03\x10\x00how me t',
        b'F\x00\x00 \x00*\x00\x04\x80\x11(\x9a\x7f\x00\x00\x01\x7f\x00\x00\x01\x03\x03\x10\x00he code.'
    ]

    expected_payload = b'~\xe0\x00P\x00(\n\x05Talk is cheap. Show me the code.'
    result_payload = reassembleFragments(fragments)

    print(f"Fragments:          {fragments}")
    print(f"Resulting payload : {result_payload}")
    print(f"Expected payload:   {expected_payload}")
    print(f"Worked:             {expected_payload == result_payload}")
