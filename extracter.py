import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import init, Fore
import time
import os
import tempmng

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp_js")

init(autoreset=5)

def js_extracter(url: str, silent=False, inline = True):
    if not silent:
        print(Fore.MAGENTA + f"----------------------------------")
        print(Fore.MAGENTA + f"[JSINFO] Extracting from: {url}")
        print(Fore.MAGENTA + f"----------------------------------")

    try:
        res = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )
    except Exception as e:
        print(Fore.RED + f"\n[JSDEBUG] Failed to Fetch {url} : {e}")
        return
    
    if not silent:
        print("\n" + Fore.GREEN + f"[JSTATUS] STATUS CODE: {res.status_code}" + "\n")
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    js_urls = []

    for script in soup.find_all("script", src=True):
        js_url = urljoin(url, script["src"])
        if js_url not in js_urls:
            js_urls.append(js_url)

    for num, js_url in enumerate(js_urls, 1):
        try:
            js_res = requests.get(js_url, timeout=10)
            js_res.raise_for_status()

            filename = f"script_{num}.js"
            path = os.path.join(TEMP_DIR, filename)

            res = tempmng.make_file(path=path, txt=js_res.text)

            if res and not silent:
                print(Fore.CYAN + f"[JSTRACTER JS] Saved: {path}")

        except requests.RequestException as e:
            print(Fore.RED + f"[JSDEBUG] Failed to download {js_url}: {e}")

    if inline:
        for num, script in enumerate(soup.find_all("script", src=False)):
            stxt = script.get_text()

            if not stxt.strip():
                continue

            snm = f"inline_script_{num + 1}"
            path = os.path.join(TEMP_DIR, snm + ".js")

            time.sleep(0.05)
            res = tempmng.make_file(path=path , txt=stxt)
            if res == False:
                break

            if not silent:
                print(Fore.BLUE + f"[JSTRACTER INLINE] Saved inline JS: {path}")

    if js_urls == [] and not silent:
        print(Fore.RED + "\n[JSDEBUG] No URL found.")

    return js_urls

