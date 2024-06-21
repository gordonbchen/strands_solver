import requests

from pathlib import Path


def get_valid_words() -> list[str]:
    """Return list of all valid words."""
    word_list_path = Path("word_list.txt")

    if not word_list_path.exists():
        prep_valid_words()

    with open(word_list_path, mode="r") as f:
        text = f.read()
    words = text.split("\n")
    words.pop(-1)
    return words


def prep_valid_words() -> None:
    """Download valid words and save to txt file."""
    url = (
        "https://raw.githubusercontent.com/first20hours/"
        "google-10000-english/master/google-10000-english-usa-no-swears.txt"
    )
    response = requests.get(url)

    text = (response.content).decode(encoding="utf-8")

    words = text.split("\n")
    words.pop(-1)  # Remove final empty word.

    # Filter out words shorter than 4 letters.
    words = [word for word in words if (len(word) >= 4)]

    # Write to txt file.
    with open("word_list.txt", mode="w") as f:
        for word in words:
            f.write(f"{word}\n")


def get_adj_coords(
    curr_coord: tuple[int, int],
    letters: list[list[str]],
    traversed_coords: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Get untraversed adjacent coordinates."""
    adj_coords = [
        (i, j)
        for i in range(max(0, curr_coord[0] - 1), min(len(letters), curr_coord[0] + 2))
        for j in range(
            max(0, curr_coord[1] - 1), min(len(letters[0]), curr_coord[1] + 2)
        )
        if (i != curr_coord[0] or j != curr_coord[1])
        and ((i, j) not in traversed_coords)
    ]
    return adj_coords


def get_poss_words(
    curr_coord: tuple[int, int],
    curr_word: str,
    traversed_coords: list[tuple[int, int]],
    letters: list[list[str]],
    valid_words: list[str],
) -> list[list[tuple[int, int]]]:
    """Get all possible words that can be made."""
    poss_words = []
    for adj_coord in get_adj_coords(curr_coord, letters, traversed_coords):
        new_word = curr_word + letters[adj_coord[0]][adj_coord[1]]
        if new_word in valid_words:
            poss_words.append(new_word)

        if is_valid(new_word, valid_words):
            poss_words += get_poss_words(
                adj_coord,
                new_word,
                traversed_coords + [adj_coord],
                letters,
                valid_words,
            )

    return poss_words


def is_valid(word: str, valid_words: list[str]) -> bool:
    """Return True if the word is a possible part of a word."""
    for valid_word in valid_words:
        if valid_word.find(word) == 0:
            return True
    return False


if __name__ == "__main__":
    letters = [
        list("fmiswo"),
        list("kalirv"),  # Replace with daily letters.
        list("isiyng"),
        list("snddew"),
        list("gkacbo"),
        list("eftuqu"),
        list("iresan"),
        list("enddce"),
    ]

    valid_words = get_valid_words()

    all_poss_words = []
    for i in range(len(letters)):
        for j in range(len(letters[0])):
            poss_words = get_poss_words(
                (i, j), letters[i][j], [(i, j)], letters, valid_words
            )
            all_poss_words.append(set(poss_words))

    # Display possible words by starting letter.
    for poss_words in all_poss_words:
        print("----------")
        for word in poss_words:
            print(word)
