#!/usr/bin/env python3


import sys
import struct


def usage():
    print("%s <U+AABBCCDD>" % sys.argv[0])


NB_BITS_MAX = 21
NB_BITS_PER_BYTE = 8
NB_BITS_PER_DATA_OCTET = 6
DATA_OCTET_PFX = '10'


def octets_to_str(octets: bytes) -> str:
    return ' '.join(['%.2x' % x for x in octets])


def normalize_bin(binstr: str, target_length: int) -> str:
    return '0'*(target_length - len(binstr)) + binstr


def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    codepoint = sys.argv[1]
    if not codepoint.upper().startswith("U+"):
        usage()
        sys.exit(1)

    codepoint_hex = codepoint[2:]
    codepoint_bin = bin(int(codepoint_hex, base=16))[2:]
    
    if 1 <= len(codepoint_bin) <= 7:
        header_pfx = '0'
        nb_data_bits = 7
        nb_bytes = 1
    elif 8 <= len(codepoint_bin) <= 11:
        header_pfx = '110'
        nb_data_bits = 11
        nb_bytes = 2
    elif 12 <= len(codepoint_bin) <= 16:
        header_pfx = '1110'
        nb_data_bits = 16
        nb_bytes = 3
    elif 17 <= len(codepoint_bin) <= 21:
        header_pfx = '11110'
        nb_data_bits = 21
        nb_bytes = 4
    else:
        raise ValueError("Invalid code point")

    codepoint_bin_norm = normalize_bin(codepoint_bin, nb_data_bits)

    octets = []

    # Generate data octets
    for _ in range(nb_bytes - 1):
        data_octet_bits = codepoint_bin_norm[-NB_BITS_PER_DATA_OCTET:]
        current_octet = (DATA_OCTET_PFX + data_octet_bits)
        octets.insert(0, int(current_octet, base=2))
        codepoint_bin_norm = codepoint_bin_norm[:-NB_BITS_PER_DATA_OCTET]

    # Generate header octet
    current_octet = (header_pfx + codepoint_bin_norm)
    octets.insert(0, int(current_octet, base=2))

    print(octets_to_str(octets))


if __name__ == '__main__':
    main()

