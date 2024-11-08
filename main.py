import pandas as pd
import nltk
import random
import matplotlib.pyplot as plt
from nltk.corpus import words, brown, gutenberg
import re


# Download necessary NLTK data
nltk.download('gutenberg', quiet=True)
nltk.download('brown', quiet=True)

from Functions import (
    most_common, least_common, double_letters, has_double_letters,
    relative_frequency_df,calculate_position_frequencies, has_specific_prefix, has_specific_suffix,
    calculate_log_commonality, get_random_words
)

# Generate a DataFrame of random words from the 'gutenberg' corpus
sample_words = get_random_words('gutenberg', length=5, sample_size=50)
words_df = pd.DataFrame(sample_words, columns=['word'])

# Apply functions to extract various word characteristics and scores
words_df['most_common'] = words_df['word'].apply(most_common)
words_df['least_common'] = words_df['word'].apply(least_common)
words_df['double_letters'] = words_df['word'].apply(double_letters)
words_df['consecutive_double_letters'] = words_df['word'].apply(has_double_letters)
words_df = calculate_position_frequencies(words_df)

# Calculate total and weighted frequency scores for each word
words_df['frequency_score'] = words_df[['p1_frequency', 'p2_frequency', 'p3_frequency', 'p4_frequency', 'p5_frequency']].sum(axis=1)
words_df['weighted_frequency'] = (
    2 * words_df['p1_frequency'] +
    words_df['p2_frequency'] +
    words_df['p3_frequency'] +
    words_df['p4_frequency'] +
    2 * words_df['p5_frequency']
)

# Identify if words have specific prefixes or suffixes
words_df['prefix'] = words_df['word'].apply(has_specific_prefix)
words_df['suffix'] = words_df['word'].apply(has_specific_suffix)

# Calculate log commonality score and normalize it to a 0-1 range
words_df['log_commonality'] = words_df['word'].apply(calculate_log_commonality)
min_log, max_log = words_df['log_commonality'].min(), words_df['log_commonality'].max()
words_df['normalized_commonality'] = (words_df['log_commonality'] - min_log) / (max_log - min_log)

# Calculate difficulty score based on various word features
words_df['score'] = (
    (2 * words_df['least_common'])
    - words_df['most_common']
    + 0.5 * words_df['double_letters']
    + words_df['consecutive_double_letters']
    - words_df['frequency_score']
    - 0.5 * words_df['prefix']
    - words_df['suffix']
    - 2 * words_df['normalized_commonality']
)



# Remove NaN values in 'score' column to avoid issues with quantile calculation
words_df = words_df.dropna(subset=['score'])

# Define quantile-based difficulty levels, with adjustments if quantiles overlap
quantiles = words_df['score'].quantile([0.2, 0.6]).values
if quantiles[0] == quantiles[1]:
    bins = [words_df['score'].min(), quantiles[0], quantiles[1] + 0.01, words_df['score'].max()]
else:
    bins = [words_df['score'].min(), quantiles[0], quantiles[1], words_df['score'].max()]
labels = ['easy', 'medium', 'hard']

# Assign difficulty level based on score bins
words_df['difficulty'] = pd.cut(words_df['score'], bins=bins, labels=labels, include_lowest=True)


# Set option to display all columns in the console output
pd.set_option('display.max_columns', None)
# Display top 5 words by difficulty score (optional; uncomment to view)
print(words_df.head())
# Reset display option to default for future prints
pd.reset_option('display.max_columns')


# Sort by score before plotting
words_df = words_df.sort_values(by='score').reset_index(drop=True)

# Visualization: Scatter plot of words by score and difficulty level
plt.figure(figsize=(10, 6))
colors = {'easy': 'green', 'medium': 'orange', 'hard': 'red'}
plt.scatter(words_df['word'], words_df['score'], c=words_df['difficulty'].map(colors))

# Customize plot appearance
plt.xlabel('Words')
plt.ylabel('Score')
plt.title('Word Scores by Difficulty Level')
plt.xticks(rotation=45)
plt.legend(handles=[
    plt.Line2D([0], [0], marker='o', color='w', label='Easy', markerfacecolor='green'),
    plt.Line2D([0], [0], marker='o', color='w', label='Medium', markerfacecolor='orange'),
    plt.Line2D([0], [0], marker='o', color='w', label='Hard', markerfacecolor='red')
], title="Difficulty Levels")
plt.tight_layout()
plt.show()

# Histogram of word scores
plt.figure(figsize=(10, 6))
plt.hist(words_df['score'], bins=10, edgecolor='black', color='skyblue')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Histogram of Word Scores')
# plt.show()

# Reorder columns for CSV output, placing key columns at the beginning
column_order = ['word', 'score', 'difficulty'] + [col for col in words_df.columns if col not in ['word', 'score', 'difficulty']]
words_df = words_df[column_order]

# Export DataFrame to CSV
words_df.to_csv('words_data.csv', index=False)




