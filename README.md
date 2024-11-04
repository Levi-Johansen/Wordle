# Wordle 
words contained in the words dataframe.
dowload all three files and run them.

Data Dictionary:
The words dataframe has 17 columns:
1. Word: contains the word pulled from one of nltk's dictionaries
2. most_common: if the word contains the four most common letters A, E, T, O. Yes = 1, No = 0
3. least_common: if the word contains the four least common letters X, Z, J, Q Yes = 1, No = 0
4. double_letters: if the word has two of the same letters. Yes = 1, No = 0
5. consecutive_double_letters: if the word contains double letters next to eachother. Yes = 1, No = 0
6. p1_frequency: The frequency of the letter in that the first position. #Run print(relative_frequency_df), to see data
7. p2_frequency: ^
8. p3_frequency: ^
9. p4_frequency: ^
10. p5_frequency: ^
11. frequency_score: sum of all the frequencies
12. weighted_frequency: Sum of the frequencies with the first and last frequency having a higher weighting
13. prefix: If the word has a common prefix: "un", "de", "re", "in", "en", "pre", "im", "em", "ir", "mid". Yes = 1, No = 0
14. suffix: If the word has a common suffix: "able", "ible", "al", "ial", "ed", "en", "er", "est", "ful",
    "ic", "ing", "ion", "tion", "ation", "ition", "ity", "ty",
    "ive", "ative", "itive", "less", "ly", "ment", "ness",
    "ous", "eous", "ious", "s", "es", "y". Yes = 1, No = 0
15. common_word: If the word is in a list of most common 5 letter words. # See Most_Common_Words.py
16. score: Difficulty rating as calculated by:  2 * least_common - most_common + 0.5 * double_letters + consecutive_double_letters - 2 * frequency_score - 0.5 * prefix - suffix - 2 * common_word
17. difficulty: Hard = top 40%, Medium = middle 40%, Easy = Bottom 20%
