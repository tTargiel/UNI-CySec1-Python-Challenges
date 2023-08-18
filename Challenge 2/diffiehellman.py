# Name: Tomasz Targiel

import random


class Alice:
    p = 0
    g = 0
    a = 0

    def initialAlice(self, p: int, g: int) -> int:
        """
        Args:
            p: common prime
            g: common generator
        Returns:
            A calculated by Alice
        """
        self.p = p
        self.g = g
        a = random.randrange(p) # Choose random a (private key) of Alice
        self.a = a # <- NO TOUCHING!!!!
        return (g ** a) % p # Calculate and return A (public key) of Alice

    def keyAlice(self, b: int) -> int:
        """
        Args:
            b: B calculated by Bob
        Returns:
            the shared key k
        """
        return (b ** self.a) % self.p # Return shared key (calculated using Bob's public key B and Alice's private key a)


class Bob:
    p = 0
    g = 0
    b = 0

    def initialBob(self, p: int, g: int) -> int:
        """
        Args:
            p: common prime
            g: common generator
        Returns:
            B calculated by Bob
        """
        self.p = p
        self.g = g
        b = random.randrange(p) # Choose random b (private key) of Bob
        self.b = b # <- NO TOUCHING!!!!
        return (g ** b) % p # Calculate and return B (public key) of Bob

    def keyBob(self, a: int) -> int:
        """
        Args:
            a: A calculated by Alice
        Returns:
            the shared key k
        """
        return (a ** self.b) % self.p # Return shared key (calculated using Alice's public key A and Bob's private key b)


def exchangeKey(p: int, g: int) -> tuple[int, int]:
    """
    Args:
        p: common prime
        g: common generator
    Returns:
        simulates a Diffie-Hellman Key Exchange and returns the key of alice and the key of bob as a tuple
    """
    A = Alice.initialAlice(Alice, p, g) # Generate Alice's public key A
    B = Bob.initialBob(Bob, p, g) # Generate Bob's public key B
    
    k_alice = Alice.keyAlice(Alice, B) # Generate shared key for Alice, using Bob's public key B
    k_bob = Bob.keyBob(Bob, A) # Generate shared key for Bob, using Alice's public key A

    return k_alice, k_bob # Return both keys for Alice and Bob as a tuple of integers


if __name__ == "__main__":
    prime = 4423
    generator = 54649

    k_alice, k_bob = exchangeKey(prime, generator)
    print(f"Prime used:                 {prime}")
    print(f"Generator used:             {generator}")
    print(f"Key calculated by Alice:    {k_alice}")
    print(f"Key calculated by Bob:      {k_bob}")
    print(f"Worked:                     {k_alice == k_bob}")
