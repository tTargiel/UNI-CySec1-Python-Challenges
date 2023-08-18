# Name: Tomasz Targiel

import re


def decrypt(cipher: str, shift: int) -> str:
    '''
    Args:
        cipher: ciphertext
        shift: shift used
    Returns:
        Decrypted plaintext
    '''
    possible_chars = [chr(i) for i in range(32, 127)]
    deciphered = "" # Initialize string variable that will contain deciphered text
    for i in cipher: # For every char in ciphertext
        if i in possible_chars: # If current char exists in possible_chars list (range 32-126 sharp)
                deciphered += chr((ord(i) - shift - 32) % 95 + 32) # 95 is how many chars are in range 32-126, 32 is lower bound, first find modulo of shifted char, then make sure it's in the range
        else:
            deciphered += i # If the char was out of bounds, add non-shifted char to deciphered text (because I want to conserve every char representation)
    return deciphered


def getShift(cipher: str, en_dictionary: str) -> int:
    '''
    Args:
        cipher: ciphertext
    Returns:
        Shift that was used for this encryption
    '''
    possible_chars = [chr(i) for i in range(32, 127)]
    counterDict = {} # Initialize empty dictionary that will contain count of en_dictionary compliant words for every shift
    for i in range(1, 94): # For every possible shift
        counterDict[i] = 0 # Start with count 0 for every shift
        # plaintextList = decrypt(cipher, i).split(" ") # Same as below, but without fancy handling of special characters
        plaintextList = re.sub(r"[^a-zA-Z0-9 ]", "", decrypt(cipher, i).replace("_", " ").replace("-", " ")).split(" ") # Words in the sentence can be separated with underscore, dash or space (that's how the sentence will be divided into list), next all special characters are removed with regex
        # print(plaintextList)
        for item in plaintextList: # For every element of given list (for each shift)
            # print(item)
            if (item.lower() or item.capitalize()) in en_dictionary: # If that word (both starting with lower or capital letter) exists in en_dictionary
                counterDict[i] += 1 # Add count of properly found words
    # print(counterDict)
    return max(counterDict, key=counterDict.get) # Return key (shift) corresponding to the max value (correct words count)


if __name__ == "__main__":
    with open("en_dictionary.txt", "r") as f:
        en_dictionary = f.read()

    cipher = ":NKeIGQKeOYeGeROKf"
    expected_shift = 69
    expected_plaintext = "The cake is a lie!"

    shift = getShift(cipher, en_dictionary)
    plaintext = decrypt(cipher, shift)

    print(f"Ciphertext was:         {cipher}")
    print(f"Guessed shift is:       {shift}")
    print(f"Guessed plaintext is:   {plaintext}")
    print(f"Shift worked:           {shift == expected_shift}")
    print(f"Decrypt worked:         {plaintext == expected_plaintext}")
