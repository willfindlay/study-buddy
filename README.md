# Study Buddy

## What is it?

Study Buddy is a simple flashcard generator which parses your markdown files and generates flashcards for you. It supports sections, cards, and bullet points. Currently it does not support images.

## How to install?

1. `$ git clone`https://github.com/HousedHorse/study-buddy`
1. `cd study-buddy`
1. `sudo make install`

## How to use it?

Once you have installed, just run `$ study-budy <file.md>`.

Your markdown file should look like the following:

```{md}
# Section Name

## Card Name

- point 1
- point 2

## Card Name

- point 1
- point 2

etc.
```
