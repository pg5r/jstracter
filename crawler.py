import requests
import extracter
from colorama import init, Fore
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import tldextract
import re

init(autoreset=True)

extract_queue = []
found_urls = []

def get_root_domain(url):
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}"

def normalize_url(url):
    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    if netloc.startswith("www."):
        netloc = netloc[4:]

    path = parsed.path or "/"

    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    return f"{scheme}://{netloc}{path}" + (
        f"?{parsed.query}" if parsed.query else ""
    )

def is_page_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        return False

    path = parsed.path.lower()

    if not path:
        return True

    filename = path.rsplit("/", 1)[-1]

    resource_extensions = {
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
        ".ico", ".bmp", ".tif", ".tiff", ".avif", ".heic",
        ".css", ".js", ".mjs", ".map",
        ".woff", ".woff2", ".ttf", ".otf", ".eot",
        ".mp3", ".wav", ".ogg", ".oga", ".m4a", ".aac", ".flac",
        ".mp4", ".webm", ".avi", ".mov", ".mkv", ".m4v",
        ".mpeg", ".mpg", ".3gp",
        ".pdf", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".odt", ".ods", ".odp",
        ".rtf", ".txt", ".csv",
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
        ".xz", ".tgz",
        ".exe", ".msi", ".bin", ".dmg", ".iso",
        ".apk", ".deb", ".rpm",
        ".xml", ".rss", ".atom", ".json", ".webmanifest",
        ".wasm", ".swf", ".cer", ".crt", ".pem"
    }

    if filename.endswith(tuple(resource_extensions)):
        return False

    resource_names = {
        "favicon",
        "favicon.ico",
        "robots.txt",
        "sitemap.xml",
        "manifest.json",
        "browserconfig.xml",
        "crossdomain.xml",
        "apple-touch-icon.png"
    }

    if filename in resource_names:
        return False

    return True

def crawl(first: str, silent=False, inline=True, major=True, max_pages=-1):
    global found_urls
    global extract_queue

    found_urls = []

    first = normalize_url(first)

    extract_queue.append(first)

    while extract_queue:
            
        first = normalize_url(extract_queue.pop(0))

        if first in found_urls:
            continue

        if not silent:
            print(Fore.MAGENTA + f"----------------------------------")
            print(Fore.MAGENTA + f"[JSINFO] Crawling in: {first}")
            print(Fore.MAGENTA + f"----------------------------------")

        the_root = ""
        try:
            res = requests.get(
            first,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )
        except Exception as e:
            print(Fore.RED + f"\n[JSDEBUG] Failed to Fetch {first} : {e}")
            continue
        
        if res.status_code >= 400:
            continue

        if "html" not in res.headers.get("Content-Type", "").lower():
            continue

        found_urls.append(first)

        rtxt = res.text

        if major:
            the_root = get_root_domain(first)
        else:
            parsed = urlparse(first)
            the_root = f"{parsed.scheme}://{parsed.netloc}"

        raw_urls = []

        soup = BeautifulSoup(rtxt, "html.parser")

        for tag in soup.find_all(True):
            for attr, value in tag.attrs.items():
                if not isinstance(value, str):
                    continue

                if attr.lower() in (
                    "href", "src", "action", "formaction",
                    "poster", "cite", "data", "url"
                ):
                    raw_urls.append(value)

        raw_urls.extend(
            re.findall(
                r'''(?:"|')((?:https?://|//|/|\./|\.\./)[^"'`\s<>]+)(?:"|')''',
                rtxt,
                re.IGNORECASE
            )
        )

        for raw_url in raw_urls:
            if raw_url.startswith(("javascript:", "mailto:", "tel:", "data:", "#")):
                continue

            full_url = normalize_url(urljoin(first, raw_url))
            parsed = urlparse(full_url)

            if parsed.scheme not in ("http", "https"):
                continue

            full_url = full_url.split("#")[0]

            if major:
                if get_root_domain(full_url) != the_root:
                    continue
            else:
                if parsed.netloc != urlparse(first).netloc:
                    continue

            if not is_page_url(full_url):
                continue

            full_url = normalize_url(full_url)

            if full_url not in extract_queue and not full_url in found_urls:
                extract_queue.append(full_url)

        if not max_pages == -1:
            if max_pages == 1:
                break
            else:
                max_pages -= 1

    return found_urls

