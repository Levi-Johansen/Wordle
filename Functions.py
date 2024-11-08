import nltk
import random
import pandas as pd
from nltk.corpus import brown, gutenberg
from collections import Counter
import re
import math
from functools import lru_cache

# Download necessary NLTK data
nltk.download('gutenberg', quiet=True)
nltk.download('brown', quiet=True)


def get_random_words(corpus, length=5, sample_size=50):
    """
    Fetches a random sample of unique words from the specified NLTK corpus.

    Parameters:
    corpus (str): The corpus to sample words from ('words', 'brown', or 'gutenberg').
    length (int): The length of each word (default is 5).
    sample_size (int): The number of unique words to sample (default is 50).

    Returns:
    list: A list of randomly sampled words of the specified length.
    """
    pattern = re.compile(r'^[a-zA-Z]+$')  # Pattern to match alphabetic words only

    # Select words based on the specified corpus
    if corpus == 'words':
        word_list = [word.lower() for word in words.words() if len(word) == length and pattern.match(word)]
    elif corpus == 'brown':
        word_list = [word.lower() for word in brown.words() if len(word) == length and pattern.match(word)]
    elif corpus == 'gutenberg':
        word_list = [word.lower() for word in gutenberg.words() if len(word) == length and pattern.match(word)]
    else:
        raise ValueError("Unknown corpus! Choose 'words', 'brown', or 'gutenberg'.")

    unique_words = list(set(word_list))  # Remove duplicates

    # Ensure there are enough unique words to sample
    if sample_size > len(unique_words):
        raise ValueError(f"Not enough unique words of length {length} in the corpus to sample {sample_size} words.")

    return random.sample(unique_words, sample_size)


def count(word):
    """Returns the length of the word."""
    return len(word)


def least_common(word):
    """Calculates the count of uncommon letters (x, j, z, q) in the word."""
    return word.count('x') + word.count('j') + word.count('z') + word.count('q')


def most_common(word):
    """Calculates the count of common letters (e, t, a, o) in the word."""
    return word.count('e') + word.count('t') + word.count('a') + word.count('o')


def double_letters(word):
    """Determines if the word contains any repeated letters."""
    return len(set(word)) < len(word)


def has_double_letters(word):
    """Checks if the word contains consecutive identical letters."""
    for i in range(len(word) - 1):
        if word[i] == word[i + 1]:
            return True
    return False


def get_five_letter_words(corpus, length=5, max_words=10000):
    """
    Extracts words of a specified length from an NLTK corpus and samples up to max_words.

    Parameters:
    corpus (CorpusReader): The NLTK corpus to sample words from.
    length (int): The length of each word (default is 5).
    max_words (int): Maximum number of words to sample (default is 10000).

    Returns:
    list: A list of sampled words of the specified length.
    """
    words = [word.lower() for word in corpus.words() if len(word) == length and word.isalpha()]
    return random.sample(words, min(max_words, len(words)))


# Create DataFrame for easier analysis of letter positions in five-letter words
five_letter_words = get_five_letter_words(brown)
word_df = pd.DataFrame([list(word) for word in five_letter_words],
                       columns=['Position 1', 'Position 2', 'Position 3', 'Position 4', 'Position 5'])

# Initialize a dictionary to store letter frequency counts by position
frequency_dict = {letter: [0, 0, 0, 0, 0] for letter in 'abcdefghijklmnopqrstuvwxyz'}

# Count frequencies for each letter in each position
for col in word_df.columns:
    position_index = int(col.split()[1]) - 1  # Position index (0 for Position 1, etc.)
    letter_counts = word_df[col].value_counts()
    for letter, count in letter_counts.items():
        frequency_dict[letter][position_index] += count

# Convert frequency dictionary to a DataFrame and calculate relative frequencies
frequency_df = pd.DataFrame(frequency_dict, index=['Position 1', 'Position 2', 'Position 3', 'Position 4', 'Position 5']).T
relative_frequency_df = frequency_df.div(frequency_df.sum(axis=0), axis=1)


# Functions to calculate position-specific letter frequencies
# In Functions module
def calculate_position_frequencies(words_df):
    """
    Calculates and adds frequency columns for each letter position in a word based on a relative frequency table.
    This function performs batch processing on a DataFrame of words, allowing for efficient computation of
    letter frequencies across all rows.

    Parameters:
    words_df (pd.DataFrame): A DataFrame containing a column named 'word' with words for which the position-specific
                             letter frequencies will be calculated.

    Returns:
    pd.DataFrame: The same DataFrame with additional columns for the frequency of each letter in specific positions
                  (p1_frequency, p2_frequency, p3_frequency, p4_frequency, p5_frequency).

    Example:
    # >>> words_df = pd.DataFrame({'word': ['apple', 'berry', 'cherry']})
    # >>> words_df = calculate_position_frequencies(words_df)
    # >>> print(words_df)
           word  p1_frequency  p2_frequency  p3_frequency  p4_frequency  p5_frequency
    0     apple          0.02          0.15          0.10          0.07          0.05
    1     berry          0.03          0.12          0.09          0.08          0.06
    2    cherry          0.01          0.11          0.09          0.10          0.04

    Notes:
    - This function assumes the existence of a global variable `relative_frequency_df`, which is a DataFrame
      containing frequency data for each letter at each position (from Position 1 to Position 5).
    - The function uses `fillna(0)` to handle cases where a letter does not appear in the frequency table
      for a given position.

    """
    # Map the frequency of the first letter in each word and create a new column for it
    words_df['p1_frequency'] = words_df['word'].str[0].map(relative_frequency_df['Position 1']).fillna(0)

    # Map the frequency of the second letter in each word (if present) and create a new column
    words_df['p2_frequency'] = words_df['word'].str[1].map(relative_frequency_df['Position 2']).fillna(0)

    # Map the frequency of the third letter in each word (if present) and create a new column
    words_df['p3_frequency'] = words_df['word'].str[2].map(relative_frequency_df['Position 3']).fillna(0)

    # Map the frequency of the fourth letter in each word (if present) and create a new column
    words_df['p4_frequency'] = words_df['word'].str[3].map(relative_frequency_df['Position 4']).fillna(0)

    # Map the frequency of the fifth letter in each word (if present) and create a new column
    words_df['p5_frequency'] = words_df['word'].str[4].map(relative_frequency_df['Position 5']).fillna(0)

    return words_df



# Lists of common prefixes and suffixes
prefixes = {"un", "de", "re", "in", "en", "pre", "im", "em", "ir", "mid"}
suffixes = {
    "able", "ible", "al", "ial", "ed", "en", "er", "est", "ful",
    "ic", "ing", "ion", "tion", "ation", "ition", "ity", "ty",
    "ive", "ative", "itive", "less", "ly", "ment", "ness",
    "ous", "eous", "ious", "s", "es", "y"
}


def has_specific_prefix(word):
    """Checks if the word starts with any of the specified prefixes."""
    return int(any(word.lower().startswith(prefix) for prefix in prefixes))


def has_specific_suffix(word):
    """Checks if the word ends with any of the specified suffixes."""
    return int(any(word.lower().endswith(suffix) for suffix in suffixes))


# Frequency analysis based on the Brown corpus
brown_words = [word.lower() for word in brown.words() if word.isalpha()]
brown_freq = Counter(brown_words)  # Frequency of each word in the Brown corpus

@lru_cache(maxsize=None)
def calculate_log_commonality(word):
    """
    Calculates the log commonality score of a word based on its frequency in the Brown corpus.

    Parameters:
    word (str): The word for which to calculate the commonality index.

    Returns:
    float: Log-transformed frequency of the word in the Brown corpus (0 if the word is not found).
    """
    freq = brown_freq.get(word, 0)
    return math.log(freq + 1)

