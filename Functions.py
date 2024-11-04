import nltk
import random
import pandas as pd
from nltk.corpus import brown
from collections import Counter

# Ensure the Brown corpus is downloaded
# nltk.download('brown')

def count(word):
    return len(word)

word = 'apiplez'
def least_common(word):
    num = word.count('x') + word.count('j') + word.count('z') + word.count('q')
    return num
# print(least_common(word))

def most_common(word):
    num = word.count('e') + word.count('t') + word.count('a') + word.count('o')
    return num
# print(most_common(word))

def double_letters(word):
    # Create a set to track characters that have already been seen
    seen = set()

    # Loop through each character in the word
    for char in word:
        # If the character is already in the set, we found a duplicate
        if char in seen:
            return True
        # Add the character to the set if it's not already there
        seen.add(char)

    # If no duplicates are found, return False
    return False
# print(double_letters(word))

def has_double_letters(word):
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return True
    return False

# print(has_double_letters(word))


def get_five_letter_words(corpus, length=5, max_words=10000):
    # Filter for words with specified length
    words = [word.lower() for word in corpus.words() if len(word) == length and word.isalpha()]

    # Randomly sample up to max_words
    return random.sample(words, min(max_words, len(words)))


# Get up to 10,000 five-letter words from the Brown corpus
five_letter_words = get_five_letter_words(brown)

# Create a DataFrame with each letter in its own column for easier analysis
word_df = pd.DataFrame([list(word) for word in five_letter_words],
                       columns=['Position 1', 'Position 2', 'Position 3', 'Position 4', 'Position 5'])

# Initialize an empty dictionary to store frequency counts
frequency_dict = {letter: [0, 0, 0, 0, 0] for letter in 'abcdefghijklmnopqrstuvwxyz'}

# Count frequencies for each letter in each position
for col in word_df.columns:
    position_index = int(col.split()[1]) - 1  # Get the position index (0 for Position 1, etc.)
    letter_counts = word_df[col].value_counts()

    for letter, count in letter_counts.items():
        frequency_dict[letter][position_index] += count

# Convert frequency dictionary to a DataFrame
frequency_df = pd.DataFrame(frequency_dict,
                            index=['Position 1', 'Position 2', 'Position 3', 'Position 4', 'Position 5']).T

relative_frequency_df = frequency_df.div(frequency_df.sum(axis=0), axis=1)

# Display the resulting relative frequency DataFrame
# print(relative_frequency_df)

# def p1_frequency(word):
#     global relative_frequency_df
#     letter = word[0]
#     freq = relative_frequency_df['Position 1'].loc[letter]
#     return freq


def p1_frequency(word):
    letter = word[0]  # Get the first letter of the word
    # Check if the letter exists in the index to avoid errors
    if letter in relative_frequency_df.index:
        freq = relative_frequency_df['Position 1'].loc[letter]
    else:
        freq = 0  # Default to 0 if the letter is not in the DataFrame
    return freq

def p2_frequency(word):
    letter = word[1] if len(word) > 1 else None  # Get the second letter of the word
    if letter and letter in relative_frequency_df.index:
        freq = relative_frequency_df['Position 2'].loc[letter]
    else:
        freq = 0  # Default to 0 if the letter is not in the DataFrame
    return freq

def p3_frequency(word):
    letter = word[2] if len(word) > 2 else None  # Get the third letter of the word
    if letter and letter in relative_frequency_df.index:
        freq = relative_frequency_df['Position 3'].loc[letter]
    else:
        freq = 0  # Default to 0 if the letter is not in the DataFrame
    return freq

def p4_frequency(word):
    letter = word[3] if len(word) > 3 else None  # Get the fourth letter of the word
    if letter and letter in relative_frequency_df.index:
        freq = relative_frequency_df['Position 4'].loc[letter]
    else:
        freq = 0  # Default to 0 if the letter is not in the DataFrame
    return freq

def p5_frequency(word):
    letter = word[4] if len(word) > 4 else None  # Get the fifth letter of the word
    if letter and letter in relative_frequency_df.index:
        freq = relative_frequency_df['Position 5'].loc[letter]
    else:
        freq = 0  # Default to 0 if the letter is not in the DataFrame
    return freq

# List of prefixes


# List of the ten specific prefixes to check
prefixes = ["un", "de", "re", "in", "en", "pre", "im", "em", "ir", "mid"]


def has_specific_prefix(word):
    word = str(word)
    word.lower()# Ensure word is a string

    # Check if the word starts with any of the specified prefixes
    for prefix in prefixes:
        if word.startswith(prefix):
            return 1  # Return 1 if the word has a matching prefix

    return 0  # Return 0 if no prefix matches


# List of specified suffixes
suffixes = [
    "able", "ible", "al", "ial", "ed", "en", "er", "est", "ful",
    "ic", "ing", "ion", "tion", "ation", "ition", "ity", "ty",
    "ive", "ative", "itive", "less", "ly", "ment", "ness",
    "ous", "eous", "ious", "s", "es", "y"
]


def has_specific_suffix(word):
    word = str(word).lower()  # Ensure word is a lowercase string

    # Check if the word ends with any of the specified suffixes
    for suffix in suffixes:
        if word.endswith(suffix):
            return 1  # Return 1 if the word has a matching suffix

    return 0  # Return 0 if no suffix matches

from Most_Common_Words import words_5_letters

def common_word(word):
    if word in words_5_letters:
        return True
    else:
        return False



