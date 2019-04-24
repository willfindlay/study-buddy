# Study Buddy

## What is it?

Study Buddy is a study tool which parses your markdown files and generates flashcards for you. It supports cards with titles, subtitles, subsubtitles, subsubsubtitles, bulleted points, numbered points, and plaintext.

Currently, it does not support images (and I have no plans to add image support as iamges really don't belong on flashcards).

## Requirements

1. python3
1. pip3
1. fpdf (installed with the included Makefile)

## How to install?

### GNU/Linux

1. `$ git clone https://github.com/HousedHorse/study-buddy`
1. `$ cd study-buddy`
1. `$ sudo make install`

### MacOS

1. `$ git clone https://github.com/HousedHorse/study-buddy`
1. `$ cd study-buddy`
1. `$ sudo make mac-install`

## How to use it?

Once you have installed the script, just run `$ study-buddy <file.md>`.

Optional parameters exist to set the number of spaces per indent in your original markdown file (default 4) and to set a location and name for the output file (default flashcards.pdf).

Your markdown file should look like the following:

``` markdown
# A Card

## First Subtitle

- here's a bullet
    - here's another bullet
        - and a third bullet

## A Second Subtitle

- this application is pretty cool
- well, it's more of a script
- oh well, it's cool anyway

# Another Card

1. Write a numbered point
1) Use another way of writing a numbered point
7. ???
(7) Profit

# Many Titles

## Sub

Here is some plaintext

### Subsub

#### Subsubsub

## Another Sub

```
