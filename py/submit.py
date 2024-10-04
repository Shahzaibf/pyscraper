from urllib.request import urlopen


def urlChecker(url):
    if url[:8] != "https://":
        return False
    else:
        return True


def onSubmit(url):
    urll = url
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("UTF-8")
    return html
