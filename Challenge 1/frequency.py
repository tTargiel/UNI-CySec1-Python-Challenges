# Name: Tomasz Targiel


def countLetters(text: str) -> dict[str, int]:
    '''
    Args:
        text: Self-explanatory

    Returns:
        Dictionary with number of occurrences for every letter (as lowercase)
    '''
    text = text.lower() # Make sure that all characters are lowercase
    dict={} # Initialize empty dictionary
    for i in range(97,123): # Iterate through ASCII table values (lowercase letters)
        counter = text.count(chr(i)) # Check how many of current i-iteration chars are in the text
        dict[chr(i)] = 0 + counter # Add occurrences count to the key
    return dict


def convertToFrequency(letter_counts: dict[str, int]) -> dict[str, float]:
    '''
    Args:
        letter_counts: Dictionary with number of occurrences for every letter (as lowercase)

    Returns:
        Dictionary with the frequency of occurrence for every letter (as lowercase)
    '''
    noLetters = sum(letter_counts.values()) # Count how many letters (not characters!) given text has
    for i in letter_counts: # For every key in dictionary
        letter_counts[i] = letter_counts[i]/noLetters # Change value of every key to the true frequency of that letter in the given text
    return letter_counts


def plotLetterFreq(frequencies: dict[str, float], file=None) -> None:
    '''
    JUST FOR FUN! NOT IMPORTANT FOR THE TASK!
    Args:
        frequencies: Dictionary with the frequency of occurrence for every letter
        file: [Optional] If specified, the graphic is not displayed, but saved in a file with this name
    '''
    try:
        matplotlib = __import__("matplotlib", fromlist=["pyplot"])
        plt = matplotlib.pyplot
        labels = frequencies.keys()

        plt.bar(range(len(labels)), frequencies.values(), tick_label=list(labels))
        if file:
            plt.savefig(file)
        else:
            plt.show()
    except Exception as e:
        print(f"An error occurred while plotting: {e}")
        if "matplotlib" in str(e):
            print(f"Is matplotlib installed? If not use 'pip install matplotlib' to install it!")


if __name__ == "__main__":
    text = "H3llo World!"
    print(f"The text was:           {text}")

    letter_counts = countLetters(text)
    print(f"The letter counts are:  {letter_counts}")

    frequencies = convertToFrequency(letter_counts)
    print(f"The frequencies are:    {frequencies}")

    # plotLetterFreq(frequencies) # Just for fun!
