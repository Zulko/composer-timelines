import re
import json

from urllib.parse import unquote
from bs4 import BeautifulSoup
from fastprogress import progress_bar

from .io_utils import cached_web_request

IMSLP_URL = "https://imslp.org"


def _detect_imslp_url(wikipedia_html):
    soup = BeautifulSoup(wikipedia_html, features="lxml")
    for link in soup.select("a"):
        if "href" in link.attrs:
            href = link.attrs["href"]
            if href.startswith(IMSLP_URL + "/wiki/Category"):
                return href


def _get_work_data_from_imslp_html(imslp_html, composer):
    composer_underscore = composer.replace(" ", "_")
    matches = re.findall(r'.extend\(catpagejs,\{"p1":(\{[^}]+\})', imslp_html)
    match = json.loads(matches[0])

    works = [
        work.split("|")[0] for letter_list in match.values() for work in letter_list
    ]
    works_data = [
        {
            "title": work.replace(f"({composer})", "").strip(),
            "imslp_url": f"{IMSLP_URL}/wiki/{work.replace(' ', '_')}",
        }
        for work in works
    ]
    return [work for work in works_data if composer_underscore in work["imslp_url"]]


def _get_publication_year(work_html):
    def detect_year(txt):
        # Regular expression to find all numbers in the text
        numbers = re.findall(r"\b\d{4}\b", txt)
        for num in numbers:
            year = int(num)
            if 1000 <= year <= 3000:
                return year
        return None

    try:
        soup = BeautifulSoup(work_html, features="lxml")
    except:
        return None
    indicators = ["First Publication", "Composition Year"]
    trs = [
        tr
        for tr in soup.select("tr")
        if any([indicator in tr.get_text() for indicator in indicators])
    ]
    if trs == []:
        return None
    year = trs[0].select("td")[0].get_text()
    return detect_year(year)


def get_works_data_from_imslp(composer_data):
    wikipedia_url = composer_data["wikipedia_url"]
    wikipedia_html = cached_web_request(wikipedia_url)

    imslp_url = _detect_imslp_url(wikipedia_html)
    if imslp_url is None:
        works_data = []
    else:
        imslp_html = cached_web_request(imslp_url)
        composer = re.findall("Category:(.*)</h1>", imslp_html)[0].strip()
        works_data = _get_work_data_from_imslp_html(imslp_html, composer)
        for work in progress_bar(works_data):
            work_html = cached_web_request(work["imslp_url"])
            work["year"] = _get_publication_year(work_html)
    return works_data
