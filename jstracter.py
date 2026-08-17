#!/usr/bin/env python3

from colorama import init, Fore
import os
import argparse
import crawler
import extracter
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_js")

header = r"""
      _     _                  _            
     | |___| |_ _ __ __ _  ___| |_ ___ _ __ 
  _  | / __| __| '__/ _` |/ __| __/ _ \ '__|
 | |_| \__ \ |_| | | (_| | (__| ||  __/ |   
  \___/|___/\__|_|  \__,_|\___|\__\___|_|                               
"""

help = """
JStracter - JavaScript URL Extractor & Web Crawler

Usage:
jstracter.py -u <URL> -o <OUTPUT> [OPTIONS]

Required arguments:
-u, --url <URL>             Target URL to crawl or analyze.
-o, --output <PATH>         Directory where extracted results will be stored.

Options:
-s, --silent                Run silently without verbose output.
-c, --count <NUMBER>        Maximum number of pages to crawl.
Default: -1 (unlimited).

```
-nc, --no-crawl, --nocrawl  Disable crawling and process only the
                            specified URL.

-ni, --no-inline, --noinline
                            Disable extraction from inline JavaScript.

-m, --major                 Enable major-page crawling mode.

-h, --help                  Explains the tool usage.
```

Examples:
jstracter.py -u https://example.com -o ./results

```
jstracter.py -u https://example.com -o ~/Desktop/results -c 100

jstracter.py -u https://example.com -o ./results --no-crawl

jstracter.py -u https://example.com -o ./results --no-inline

jstracter.py -u https://example.com -o ./results -s -c 50

jstracter.py -u https://example.com -o ./results -m
```

"""


init(autoreset=5)

def start():
    global help

    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("-u", "--url")
    parser.add_argument("-o", "--output", type=str)
    parser.add_argument("-s", "--silent", action="store_true")
    parser.add_argument("-c", "--count", type=int, default=-1)
    parser.add_argument("-nc", "--no-crawl" , "--nocrawl", action="store_true")
    parser.add_argument("-ni", "--no-inline" , "--noinline", action="store_true")
    parser.add_argument("-m", "--major", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")

    args = parser.parse_args()

    is_help = False
    if args.help and args.help == True:
        is_help = True
        print(header)
        print(help)

    errs = 0

    if not args.output:
        if not is_help:
            print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: missing argument -o(output).")
        errs += 1
    
    if not args.url:
        if not is_help:
            print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: missing argument -u(url).")
        errs += 1

    if errs > 0:
        return

    folder = os.path.basename(os.getcwd())
    if folder == "temp_js":
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: can't run the tool in a folder named 'temp_js'.")
        return

    if args.output == "temp_js":
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: the output can't be in a folder named 'temp_js'.")
        return

    url = args.url
    silent = args.silent
    crawl = not args.no_crawl
    mmax = args.count
    output = args.output
    inline = not args.no_inline
    major = args.major

    if not os.path.isfile(os.path.join(BASE_DIR, "extracter.py")):
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: file 'extracter.py' not found.")
        return
    if not os.path.isfile(os.path.join(BASE_DIR, "crawler.py")):
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: file 'crawler.py' not found.")
        return
    if not os.path.isfile(os.path.join(BASE_DIR, "tempmng.py")):
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: file 'tempmng.py' not found.")
        return
    if not os.path.isdir(TEMP_DIR):
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: folder 'temp_js/' not found.")
        return

    if not str(url).startswith("https://") and not str(url).startswith("http://"):
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: the url must start with a valid scheme like: 'https://example.com' or 'http://example.com'.")
        return

    print(Fore.LIGHTYELLOW_EX + f"\n{header}")

    urls = []

    if crawl:
        res = crawler.crawl(first=url , silent=silent , inline=inline , major=major , max_pages= mmax)
        if not isinstance(res, list):
            return
        urls = res
    else:
        urls.append(url)

    for url in urls:
        extracter.js_extracter(url=url , silent=silent , inline=inline)

    try:
        output_path = os.path.expanduser(output)
        parent = os.path.dirname(output_path) or "."

        os.makedirs(parent, exist_ok=True)

        shutil.move(TEMP_DIR, output_path)
        os.mkdir(TEMP_DIR)

    except Exception as e:
        print(Fore.RED + f"\n[JSDEBUG] FATAL ERROR: failed to make the output folder: {e}")
        return

    print(Fore.GREEN + f"\nOperation ended Successfuly !")
    
start()
