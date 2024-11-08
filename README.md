# Wordle 
This program analyzes a set of randomly selected words from the NLTK corpus and assigns each word a difficulty score based on various word characteristics. The program outputs these words and their scores in a structured DataFrame, making them easy to analyze.

### Prerequisites
To run this program, ensure you have the following Python packages installed: pandas, nltk, and matplotlib.

If these packages are not installed, use pip to install them.

### Setup
Download all required files, Functions.py and the main script.
Place all files in the same directory.
Run the main script to execute the word analysis.
How to Run
To run the program, execute the main script. This will process the data, calculate scores, and output both a CSV file (words_data.csv) and two plots.

The CSV file (words_data.csv) contains the results, and the plots show a visualization of word difficulty levels.

### Data Dictionary
The output DataFrame, words_df, contains the following 17 columns:

word: The word sampled from the NLTK corpus.

most_common: Indicates if the word contains any of the four most common letters: A, E, T, or O. A value of 1 indicates "yes," and 0 indicates "no."

least_common: Indicates if the word contains any of the four least common letters: X, Z, J, or Q. A value of 1 indicates "yes," and 0 indicates "no."

double_letters: Indicates if the word contains any repeated letters. A value of 1 indicates "yes," and 0 indicates "no."

consecutive_double_letters: Indicates if the word contains consecutive identical letters. A value of 1 indicates "yes," and 0 indicates "no."

p1_frequency: Frequency of the letter in the first position. To see this data, print relative_frequency_df.

p2_frequency: Frequency of the letter in the second position.

p3_frequency: Frequency of the letter in the third position.

p4_frequency: Frequency of the letter in the fourth position.

p5_frequency: Frequency of the letter in the fifth position.

frequency_score: Sum of the position-specific letter frequencies from p1_frequency to p5_frequency.

weighted_frequency: A weighted sum of frequencies, where the first and last position frequencies receive a higher weight.

prefix: Indicates if the word has a common prefix such as "un," "re," or "pre." A value of 1 indicates "yes," and 0 indicates "no."

suffix: Indicates if the word has a common suffix such as "able," "ed," or "ing." A value of 1 indicates "yes," and 0 indicates "no."

common_word: Indicates if the word is in the most common 5-letter words list, which can be found in Most_Common_Words.py. A value of 1 indicates "yes," and 0 indicates "no."

score: A calculated difficulty rating based on several word characteristics. The formula used is:

2 * least_common - most_common + 0.5 * double_letters + consecutive_double_letters - 2 * frequency_score - 0.5 * prefix - suffix - 2 * common_word

difficulty: The difficulty level based on the score percentile. Words in the top 40% of scores are labeled "Hard," the middle 40% are labeled "Medium," and the bottom 20% are labeled "Easy."
Example Input and Output
Example Input:

The input is a randomly selected set of words, each of five letters, from an NLTK corpus (such as gutenberg, brown, or words). The sample size and word length can be adjusted in the code.

### Example Output:

The output is a DataFrame with columns as described in the Data Dictionary. For instance, an example word, "apple," might have values like these:

word: "apple"

most_common: 1

least_common: 0

double_letters: 1

consecutive_double_letters: 1

p1_frequency: 0.02

p2_frequency: 0.15

p3_frequency: 0.10

p4_frequency: 0.07

p5_frequency: 0.05

frequency_score: 0.39

weighted_frequency: 0.52

prefix: 0

suffix: 0

common_word: 0

score: -0.8

difficulty: Medium

### Usage Notes

Data Sampling: You can adjust the sample size and length of the words by modifying the parameters in get_random_words(corpus, length, sample_size).

Frequency Analysis: The relative_frequency_df provides frequency values for each letter by position, used in the p1_frequency through p5_frequency columns.

Difficulty Score Calculation: The score is calculated based on several word characteristics. Higher scores indicate higher difficulty, and the score is then categorized into Easy, Medium, or Hard.

Output Visualization: The program generates two plots:

A scatter plot displaying words by difficulty score and assigned difficulty level.
A histogram showing the distribution of difficulty scores.
Additional Information
The final DataFrame is saved as words_data.csv, which can be used for further analysis or visualization as needed.


