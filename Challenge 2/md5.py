# Name: Tomasz Targiel

from math import floor, sin, ceil


class MD5():
    # S specifies the per-round shift amounts
    S = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14,
         20, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6,
         10, 15, 21]

    # Use binary integer part of the sines of integers(Radians) as constants:
    K = [floor(2 ** 32 * abs(sin(i + 1))) for i in range(0, 64)]

    BLOCK_SIZE = 64  # Bytes (= 512 bits)

    # Initialize variables:
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    def loadState(self, hash):
        '''
        Stores given hash as the current internal state (Initialize variables)
        Args:
            hash: hex representation of the hash as a string (without 0x)
        '''
        hash_int = int(hash, base=16)
        result_bytes = hash_int.to_bytes(16, "big")
        result_sum = int.from_bytes(result_bytes, "little")
        self.a0 = result_sum & 0xffffffff
        self.b0 = (result_sum >> 32) & 0xffffffff
        self.c0 = (result_sum >> 64) & 0xffffffff
        self.d0 = (result_sum >> 96) & 0xffffffff

    def hash(self, message):
        '''
        Args:
            message: of Type string or bytes (no limitations in size)

        Returns:
            hex representation of the hash as a string (without 0x)
        '''
        if type(message) == str:
            byte_array = bytearray(message, "ascii")
        if type(message) == bytes:
            byte_array = bytearray(message)

        # Preprocessing
        padded_byte_array = self.addPadding(byte_array)

        # Start hashing
        hash = self.runHashAlgo(padded_byte_array)
        return hash

    def addPadding(self, byte_array):
        '''
        Adds MD5 specific padding to bytearray
        Args:
            byte_array: message to be padded as a bytearray

        Returns:
            bytearray of the message + padding
        '''

        # To append later
        original_len = len(byte_array)*8 % 2 ** 64

        # Adding a single 1 bit
        # -> since letters are fixed to 8 bits with UTF-8, we can directly append 〈10000000〉_10 (〈128〉_2)
        byte_array.append(128)

        # Padding with zeros
        while len(byte_array) % (self.BLOCK_SIZE) != 56:
            byte_array.append(0)

        # Append original length
        byte_array += original_len.to_bytes(8, "little")
        return byte_array

    def runHashAlgo(self, padded_byte_array):
        '''
        Args:
            padded_byte_array: bytearray of the message + padding

        Returns:
            hex representation of the hash as a string (without 0x)
        '''
        left_rotate = lambda x, n: (x << n) | (x >> (32 - n))

        # Split the message into blocks of BLOCK_SIZE and run algorithm on each once
        for offset in range(0, ceil(len(padded_byte_array) / self.BLOCK_SIZE)):
            current_block = padded_byte_array[self.BLOCK_SIZE * offset: self.BLOCK_SIZE * (offset + 1)]

            # Cut into 16 8 byte words
            current_blocks = [] # = To M in wiki ... but M might be a bit confusing as a name
            for i in range(0, 16):
                # Change representation from bytes to integer -> better for doing math
                value = int.from_bytes(current_block[4 * i: 4 * i + 4], 'little')
                current_blocks.append(value)

            # Initialize hash value for this chunk
            a = self.a0
            b = self.b0
            c = self.c0
            d = self.d0
            f = ""

            # Main loop
            for i in range(0, 64):
                if 0 <= i <= 15:
                    f = (b & c) | (~b & d)
                    g = i
                elif 16 <= i <= 31:
                    f = (d & b) | (~d & c)
                    g = (5 * i + 1) % 16
                elif 32 <= i <= 47:
                    f = b ^ c ^ d
                    g = (3 * i + 5) % 16
                elif 48 <= i <= 63:
                    f = c ^ (b | ~d)
                    g = (7 * i) % 16

                # % 2**32 to stay within 32 bit
                f = (f + a) % 2**32
                f = (f + self.K[i]) % 2**32
                f = (f + current_blocks[g]) % 2**32

                a = d
                d = c
                c = b
                b = (b + left_rotate(f, self.S[i])) % 2**32

            # Add this chunk's hash to result so far:
            self.a0 = (self.a0 + a) % 2**32
            self.b0 = (self.b0 + b) % 2**32
            self.c0 = (self.c0 + c) % 2**32
            self.d0 = (self.d0 + d) % 2**32

        # The real meaning of: a0 append b0 append c0 append d0
        result_sum = self.a0 + (self.b0 << 32) + (self.c0 << 64) + (self.d0 << 96)

        # Some formatting magic, because python loves to throw away starting zeros
        result_bytes = result_sum.to_bytes(16, byteorder='little') # (Output is in little-endian)
        result = '{:032x}'.format(int.from_bytes(result_bytes, byteorder='big'))
        return result


if __name__ == "__main__":
    msg = "Hash me :D"

    md5 = MD5()
    hash = md5.hash(msg)
    expected_hash = "b0250fbb5a750194568ccd5d1d8b19ef"

    print(f"Message:                {msg}")
    print(f"Hash:                   {hash}")
    print(f"Expected:               {expected_hash}")
    print(f"Worked:                 {hash == expected_hash}")
