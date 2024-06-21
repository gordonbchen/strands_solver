# strands_solver
A program to beat Evelyn at NYT's strands.

## Usage
Requirements: `python3`, `requests`

Replace the hard-coded list of letters with the daily letters (`main.py` line 97).

Run: `python3 main.py`

## Description.
* Downloads and filters a list of 10,000 most common english words, and saves the list to `word_list.txt`.
* Finds every english word hidden in the given list of letters by traversing every possible path through the letters, terminating when no english words can be made out of the visited letters.

## Sources
* NYT Strands: https://www.nytimes.com/games/strands 
* List of english words from: https://github.com/first20hours/google-10000-english
