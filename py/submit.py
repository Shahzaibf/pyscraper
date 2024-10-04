from urllib.request import urlopen
from bs4 import BeautifulSoup


def urlChecker(url):
    if url[:8] == "https://" or url[:4] == "www.":
        return True
    else:
        return False


def onSubmit(url):
    urll = url
    try:
        page = urlopen(url)
    except:
        return "INVALID URL. Forbidden"
    html_bytes = page.read()
    html = html_bytes.decode("UTF-8")
    soup = BeautifulSoup(html, 'html.parser')
    return soup
