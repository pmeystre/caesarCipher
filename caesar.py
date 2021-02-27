import string
import time
from rich.console import Console
from rich.table import Table
import nltk
from nltk.corpus import words
from operator import itemgetter


def main():
    start_time = time.time()
    ciphered_text = input(str('Enter text to decipher: '))
    try_iterations(message=ciphered_text)
    end_time = time.time() - start_time
    print(f"Execution time: {end_time} seconds")


def try_iterations(message):
    """

    :param message: Takes the user inputted ciphered text
    :return:
    """
    table_rows = []  # Creates a table to store results
    offset = 1  # Sets first iterator
    print('working...')
    for i in range(24):  # Loop through all 25 possible shifts
        deciphered_text, wordcount = decipher(offset, message)  # Gets deciphered string and number of english words in that string
        table_rows.append([offset, deciphered_text, wordcount])  # Appends result to row
        offset += 1  # Move onto the next iteration
    table_rows.sort(key=itemgetter(2), reverse=True)  # Sort results by word count key
    pretty_print(data=table_rows[:1])  # Display the best result as a table


def decipher(offset, message):
    """
    :param offset: Current iteration of the script. Refers to how the number of digits the alphabet is shifted
    :type offset: int
    :param message: The string to decipher
    :type message: str
    :return: Returns deciphered string, number of words found in the english dictionary
    """
    result_string = ""  # Start with an empty string
    text = list(message.lower())  # Get the list version of the strong
    alphabet = list(string.ascii_lowercase)  # Create a list that contains each letter of the alphabet
    offset_alphabet = alphabet[offset:] + alphabet[:offset]  # Create a list that starts at the offset ordinal position of the alphabet list
    for index, value in enumerate(text):  # Iterate over each character in the ciphered text
        if value.isalnum():  # If the value of the character is alpha-numeric
            try:
                new_character = alphabet.index(value)  # Lookup that characters index in the alphabet
                result_string += offset_alphabet[new_character]  # Then take that index number, and lookup it's value in the shifted alphabet
            except ValueError:  # Catch weird alphanumeric exceptions, like "Hello5"
                result_string += value  # Treat them like non alphanumeric characters and hope for the best
        else:  # If the character if not alpha-numeric
            result_string += value  # Append the character to the result_string string as-is
    dict_count = count_english_words(result_string)
    return result_string, dict_count


def count_english_words(string_to_process):
    """

    :param string_to_process: Processes deciphered sting
    :return: Number of words in the dictionary for string
    """
    dict_count = 0
    word_set = set(words.words())  # Using set method speeds up execution time significantly
    tokenized_text = nltk.word_tokenize(string_to_process, language="english")  # Tokenize string
    for tokenized_index, tokenized_value in enumerate(tokenized_text):  # Iterate dictionary search over each element in tokenized string
        if tokenized_value in word_set:
            dict_count += 1
    return dict_count


def pretty_print(data):
    """

    :param data: final results
    :type data: list
    :return: Nothing, prints table to console
    """
    table = Table(title="Best 5 Results", show_lines=True)
    table.add_column("Result", no_wrap=False, justify="left", style="light_sky_blue1", header_style="bold")
    table.add_column("Word Count", no_wrap=True, justify="center", style="grey100")
    for index, value in enumerate(data):
        table.add_row(str(value[1]), str(value[2]))
    console = Console()
    console.print(table)


if __name__ == '__main__':
    main()