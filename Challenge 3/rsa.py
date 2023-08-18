# Name: Tomasz Targiel


def encrypt(m: int, e: int, n: int) -> int:
    """
    Args:
        m: message
        e: key
        n: You know this one
    Returns:
        c
    """
    c = pow(m, e, n)
    return c


def decrypt(c: int, d: int, n: int) -> int:
    """
    Args:
        c: cipher
        d: key
        n: You know this one
    Returns:
        m
    """
    m = pow(c, d, n)
    return m


def gcd(x: int, y: int) -> int:
    '''
    Args:
        x: You should know this one!
        y: This one too!
    Returns:
        greatest common divisor
    '''
    while y != 0:
        x, y = y, x % y
    return x


def extendedEuclideanAlgorithm(x: int, y: int) -> tuple[int, int, int]:
    '''
    Extended Euclidean Algorithm
    Args:
        x: You should know this one!
        y: This one too!
    Returns:
        (d, a, b) -> d = x * a + y * b and d = gcd(x, y)
    '''
    # Base case
    if x == 0:
        return y, 0, 1

    gcd, a1, b1 = extendedEuclideanAlgorithm(y % x, x)

    # Update a and b using results of recursive call
    a = b1 - (y // x) * a1
    b = a1
    d = gcd

    return d, a, b


def calculateKeys(p: int, q: int, e: int) -> tuple[tuple[int, int], tuple[int, int, int]]:
    '''
    Args:
        p: a prime
        q: a prime
        e: part of pk
    Returns:
        (pk, sk) with pk:= (n, e) and sk:= (p, q, d) or None if e is not valid
    '''
    # Calculate N
    n = p * q
    
    # Calculate Euler's totient function
    phi = (p - 1) * (q - 1)

    # Check if e is valid
    if gcd(phi, e) != 1:
        return None

    # Calculate d using extended Euclidean algorithm
    d = extendedEuclideanAlgorithm(phi, e)[1]
    
    # Return public and secret keys
    return ((n, e), (p, q, d))


if __name__ == "__main__":
    # Test part 1
    e, d, n = 7, 43, 77
    m = 9
    c = 37

    result_c = encrypt(m, e, n)
    result_m = decrypt(c, d, n)
    print(f"encrypt({m}, {e}, {n}) = {result_c} and should be {c}, so it {'worked!' if c == result_c else 'did not work!'}")
    print(f"decrypt({c}, {d}, {n}) = {result_m} and should be {m}, so it {'worked!' if m == result_m else 'did not work!'}")

    # Test part 2
    x, y = 12, 8
    expected_gcd = 4
    result_gcd = gcd(x, y)
    print(f"gcd({x}, {y}) = {result_gcd} and should be {expected_gcd}, so it {'worked!' if expected_gcd == result_gcd else 'did not work!'}")

    # Test part 3
    x, y = 10, 7
    expected_eea = (1, -2, 3)
    result_eea = extendedEuclideanAlgorithm(x, y)
    print(f"extendedEuclideanAlgorithm({x}, {y}) = {result_eea} and should be {expected_eea}, so it {'worked!' if expected_eea == result_eea else 'did not work!'}")

    # Test part 4
    p, q = 3, 11
    e = 17
    expected_keys = ((33, 17), (3, 11, 6))
    result_keys = calculateKeys(p, q, e)
    print(f"calculateKeys({p}, {q}, {e}) = {result_keys} and should be {expected_keys}, so it {'worked!' if expected_keys == result_keys else 'did not work!'}")
