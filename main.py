#!/usr/bin/env python
import random
import sys
import time
import argparse
from typing import Tuple

''' Displays the account lockout timer for the given number of seconds. '''


def lockout(timer: int):
    for i in range(timer, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Account locked for {:d} seconds.".format(i))
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r")
    sys.stdout.write(
        "You may attempt logging in once more. Password is re-encrypted.")
    sys.stdout.flush()


''' Chooses a word from the given list and returns the word and its length. '''


def get_word(words: list[str]) -> Tuple[str, int]:
    answer = random.choice(words)
    return answer, len(answer) + 1


''' Checks if the guess is the same as the answer, returning the wordle squares, if the word is correct, and the alphabet. '''


def check_word(guess: str, answer: str, alphabet: list[list[str]], colors: dict[str, str]) -> Tuple[str, bool, list[list[str]]]:
    correct = 0
    result = ""
    for i, char in enumerate(guess):
        if char in answer:
            if answer[i] == char:
                result += colors["green"]
                correct += 1
            else:
                result += colors["yellow"]
        else:
            result += colors["red"]
            upper = char.upper()
            # Greys out a letter in the alphabet
            for row, letters in enumerate(alphabet):
                try:
                    i = letters.index(upper)
                    alphabet[row][i] = "_"
                except ValueError:
                    continue
    # Rendering the alphabet
    for row, letters in enumerate(alphabet):
        print(row * " ", end=" ")
        for letter in letters:
            print("{}".format(letter), end=" ")
        print("\n")
    return (result, correct == len(answer), alphabet)


''' Checks if the given value is a positive integer. '''


def check_positive_int(value) -> bool:
    val = int(value)
    if val <= 0:
        raise argparse.ArgumentTypeError(
            "%s is an invalid positive integer value" % value)
    return val


''' Creates a parser for command line arguments. '''


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parses launch options")
    parser.add_argument("--custom", help="Use custom words for answer bank",
                        action="store_true", default=False)
    parser.add_argument("--no-emoji", help="Disable emojis for compatibility",
                        action="store_true", default=False)
    parser.add_argument("--timer", help="Set retry timer", type=check_positive_int,
                        action="store", default=15)
    return parser


''' Returns all the starting values pertaining to the valid guesses and the final guess. '''


def init(answers: list[str]) -> Tuple[str, int, bool, list[list[str]]]:
    answer, max_guesses = get_word(answers)
    skip_validation = len(answer) != 5
    if skip_validation:
        print("Encrypted password is not 5 characters. Cannot enforce that attempts are valid words.")
    return answer, max_guesses, skip_validation, [[c for c in "QWERTYUIOP"], [
        c for c in "ASDFGHJKL"], [c for c in "ZXCVBNM"]]


def main():
    random.seed()
    args = init_parser().parse_args()
    colors = {
        "green": "\U0001F7E9",
        "yellow": "\U0001F7E8",
        "red": "\U0001F7E5",
    }
    if args.no_emoji:
        print("Emojis are disabled.\nO = correct\n+ = wrong place\n* = incorrect")
        colors["green"] = "O"
        colors["yellow"] = "+"
        colors["red"] = "*"
    # Reading in word bank
    with open("base.txt") as file:
        base_words = [line.rstrip() for line in file]
    with open("guesses.txt") as file:
        valid_guesses = [line.rstrip() for line in file] + base_words
    if args.custom:
        with open("custom.txt") as file:
            answers = [line.rstrip() for line in file]
        valid_guesses += answers
    else:
        answers = base_words

    answer, max_guesses, skip_validation, alphabet = init(answers)
    remaining_guesses = max_guesses
    lockdown = args.timer
    while (True):
        print("\nYou have {:d} attempt(s) before account is locked.".format(
            remaining_guesses))
        print("Enter password:")
        guess = input()
        if not skip_validation and not guess in valid_guesses:
            print("Error! Invalid password. Please try again.")
            continue
        result, correct, alphabet = check_word(guess, answer, alphabet, colors)
        # Printing out the result and the guess
        try:
            print(result)
        except UnicodeEncodeError:
            print(
                "Looks like emojis aren't supported in your terminal, run using the --no-emoji option!")
            exit(1)
        if args.no_emoji:
            print(guess)
        else:
            for c in guess:
                print(" {}".format(c), end="")
            print()
        # Checking result
        if correct:
            print("Login successful.")
            break
        else:
            remaining_guesses -= 1
            if remaining_guesses == 0:
                # If incorrect, locks user out and "re-encrypts" the password by choosing another
                print("\n\n\nCorrect password was \"{}\"".format(answer))
                lockout(lockdown)
                answer, max_guesses, skip_validation, alphabet = init(answers)
                remaining_guesses = max_guesses


if __name__ == "__main__":
    main()
