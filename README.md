# JStracter

JStracter is a CLI tool that crawls websites and extracts external and inline JavaScript files.

## Features

- Web crawling
- External JavaScript extraction
- Inline JavaScript extraction
- Root-domain crawling
- Page crawling limits
- Silent mode
- URL normalization and filtering
- Saves extracted JavaScript files to an output directory

## Installation

```
git clone https://github.com/pg5r/jstracter.git
cd jstracter
pip install -r requirements.txt
```

## Usage

For a complete list of available commands and options:

python jstracter.py -h

## Examples

python jstracter.py -u https://example.com -o ./results

python jstracter.py -u https://example.com -o ~/Desktop/results -c 100

python jstracter.py -u https://example.com -o ./results --no-crawl

python jstracter.py -u https://example.com -o ./results --no-inline

python jstracter.py -u https://example.com -o ./results -s -c 50

python jstracter.py -u https://example.com -o ./results -m

## Output

Extracted JavaScript files are stored in the specified output directory.

Example:

results/
├── script_1.js
├── script_2.js
├── script_3.js
├── inline_script_1.js
└── inline_script_2.js

## Requirements

Python 3

requests

beautifulsoup4

colorama

tldextract

Install dependencies:

pip install -r requirements.txt

## Disclaimer

JStracter is intended for authorized security research, testing, and educational purposes. Only use it on websites and systems you have permission to test.
