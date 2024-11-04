
import pandas as pd
import nltk
from nltk.corpus import stopwords
# from nltk.corpus import words
import random
import matplotlib.pyplot as plt
import re
from nltk.corpus import words, brown, gutenberg

# Download the words corpus if you haven't done so already
# nltk.download('words')

# Load the list of words
# word_list = words.words()

# Display the first 10 words as an example
# print(word_list[:10])



# five_letter_words = [word.lower() for word in word_list if len(word) == 5]

# Select the first 50 words as an example (assuming they’re common enough)
# sample_five_letter_words = random.sample(five_letter_words, 50)

# print(sample_five_letter_words)

def get_random_words(corpus, length=5, sample_size=50):
    # Define a regular expression to match words with only alphabetic characters
    pattern = re.compile(r'^[a-zA-Z]+$')

    # Select words based on the specified corpus
    if corpus == 'words':
        word_list = [word.lower() for word in words.words() if len(word) == length and pattern.match(word)]
    elif corpus == 'brown':
        word_list = [word.lower() for word in brown.words() if len(word) == length and pattern.match(word)]
    elif corpus == 'gutenberg':
        word_list = [word.lower() for word in gutenberg.words() if len(word) == length and pattern.match(word)]
    else:
        raise ValueError("Unknown corpus! Choose 'words', 'brown', or 'gutenberg'.")

    # Remove duplicates by converting the list to a set, then back to a list
    unique_words = list(set(word_list))

    # Ensure there are enough unique words to sample
    if sample_size > len(unique_words):
        raise ValueError(f"Not enough unique words of length {length} in the corpus to sample {sample_size} words.")

    # Randomly select the specified number of unique words
    return random.sample(unique_words, sample_size)

# Example usage: Get 50 random five-letter unique words from the Gutenberg corpus
sample_words = get_random_words('gutenberg', length=5, sample_size=50)
# print(sample_words)

from Functions import (most_common, least_common, double_letters,
                       has_double_letters, relative_frequency_df, p1_frequency, p2_frequency,
                       p3_frequency, p4_frequency, p5_frequency, has_specific_prefix, has_specific_suffix,
                       common_word)

words = pd.DataFrame(sample_words, columns=['word'])

# Apply the count function to each word in the 'word' column
words['most_common'] = words['word'].apply(most_common)
words['least_common'] = words['word'].apply(least_common)
words['double_letters'] = words['word'].apply(double_letters)
words['consecutive_double_letters'] = words['word'].apply(has_double_letters)
words['p1_frequency'] = words['word'].apply(p1_frequency)
words['p2_frequency'] = words['word'].apply(p2_frequency)
words['p3_frequency'] = words['word'].apply(p3_frequency)
words['p4_frequency'] = words['word'].apply(p4_frequency)
words['p5_frequency'] = words['word'].apply(p5_frequency)
words['frequency_score'] = words[['p1_frequency', 'p2_frequency', 'p3_frequency', 'p4_frequency', 'p5_frequency']].sum(axis=1)
words['weighted_frequency'] = (
    2 * words['p1_frequency'] +
    words['p2_frequency'] +
    words['p3_frequency'] +
    words['p4_frequency'] +
    2 * words['p5_frequency']
)
words['dif'] = words['weighted_frequency'] - words['frequency_score']
words['prefix'] = words['word'].apply(has_specific_prefix)
words['suffix'] = words['word'].apply(has_specific_suffix)
words['common_word'] = words['word'].apply(common_word)

# difficulty score
words['score'] = (( 2 * words['least_common']) - words['most_common']  + .5 * words['double_letters']
                  + words['consecutive_double_letters'] - 2 * words['frequency_score']
                  - .5 * words['prefix'] -  words['suffix'] - 2 * words['common_word'])
# Set option to display all columns

print(words.sort_values(by='score', ascending=False).head())
pd.set_option('display.max_columns', None)

# Print the first few rows (e.g., first 5 rows) of the DataFrame
# Sort by 'prefix_frequency' and display the top 10 rows
# print(words.sort_values(by='prefix_frequency', ascending=False).head(10))
print('The ten easiest words are:')
print(words.sort_values(by='score', ascending=True)['word'][0:10])

print('\nThe ten hardest words are:')
print(words.sort_values(by='score', ascending=False)['word'][0:10])

# Reset the option if you don't want to keep it for future prints
pd.reset_option('display.max_columns')
# print(relative_frequency_df)
# print(words['dif'].describe())

##### Dificulty score ####

# Assuming you have a DataFrame named 'words' with columns 'word' and 'score'
# Define the bins based on the quantile cutoffs


# Assuming 'words' DataFrame is already defined with 'word' and 'score' columns
# Get quantile values
# Drop NaN values in 'score' to avoid issues with quantiles
words = words.dropna(subset=['score'])

# Get quantile values, ensuring they are strictly increasing
quantiles = words['score'].quantile([0.2, 0.6]).values

# Adjust bins if quantiles are identical
if quantiles[0] == quantiles[1]:
    bins = [words['score'].min(), quantiles[0], quantiles[1] + 0.01, words['score'].max()]
else:
    bins = [words['score'].min(), quantiles[0], quantiles[1], words['score'].max()]

# Define labels for each bin
labels = ['easy', 'medium', 'hard']

# Apply pd.cut with the adjusted bins
words['difficulty'] = pd.cut(words['score'], bins=bins, labels=labels, include_lowest=True)

# Display the resulting DataFrame to verify
print(words.head())

words = words.sort_values(by='score').reset_index(drop=True)
# Plotting
plt.figure(figsize=(10, 6))
colors = {'easy': 'green', 'medium': 'orange', 'hard': 'red'}
plt.scatter(words['word'], words['score'], c=words['difficulty'].map(colors))

# Customizing plot
plt.xlabel('Words')
plt.ylabel('Score')
plt.title('Word Scores by Difficulty Level')
plt.xticks(rotation=45)
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label='Easy', markerfacecolor='blue'),
                    plt.Line2D([0], [0], marker='o', color='w', label='Medium', markerfacecolor='orange'),
                    plt.Line2D([0], [0], marker='o', color='w', label='Hard', markerfacecolor='red')],
           title="Difficulty Levels")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
plt.hist(words['score'], bins=10, edgecolor='black', color='skyblue')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Histogram of Word Scores')
# plt.show()


