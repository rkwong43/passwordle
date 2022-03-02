# Passwordle

Little Wordle clone that can be played infinitely through the command line.

## Installation and Running

Install `Python3`.

**Note**: This will only run on consoles that are compatible with unicode emojis. I personally used VS Code's Git Bash.
`--no-emoji` option will allow its use with all consoles.

On Windows, run:

```sh
py main.py
```

For the base game.

Using the `--custom` option will use the custom text file word bank instead of the usual Wordle bank.

```sh
py main.py --custom
```

Using the `--timer` option will set the lockout timer after failing. Default is 30 seconds.

```sh
# Setting timer to 15 seconds
py main.py --timer 15
```

## Playing the Game

Like classic Wordle, guesses are checked and a string of squares determining correct placement of letters is printed out.

The `custom.txt` file can be edited to have a custom word bank. Words that are not 5 letters *can* be used, but guesses will not be checked if valid.

If the maximum number of guesses is reached, the player is locked out of the account, and will have to wait to try again. A new password to guess is chosen.
