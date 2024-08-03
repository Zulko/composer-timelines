from gpt_function_decorator import gpt_function
from .io_utils import cached_web_request
from bs4 import BeautifulSoup


def _get_wikipedia_url_from_search(term):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {"action": "query", "list": "search", "srsearch": term, "format": "json"}

    data = cached_web_request(search_url, params=params, response_type="json")

    if data["query"]["search"]:
        title = data["query"]["search"][0]["title"]
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        return page_url
    else:
        print(f"No page found for {term}")
        return None


@gpt_function(retries=2)
def composer_metadata(composer, info=None) -> dict:
    """Return a dict with the following metadata for the given composer:
    {
        first_names: str,
        last_name: str,
        birth_year: int,
        death_year: int
    }
    """


def get_basic_metadata_from_wikipedia(composer_data):
    wikipedia_url = _get_wikipedia_url_from_search(composer_data["name"])
    wikipedia_html = cached_web_request(wikipedia_url)
    soup = BeautifulSoup(wikipedia_html, "html.parser")
    composer_name = soup.select_one("h1").get_text()
    content = soup.select("#bodyContent")[0]
    first_paragraphs = [p.text.strip() for p in content.find_all("p")[:3]]
    metadata = composer_metadata(composer_name, info=" ".join(first_paragraphs))
    return {
        "full_name": composer_name,
        "wikipedia_url": wikipedia_url,
        **metadata,
    }


def _extract_sections_from_wikipedia_page(
    html_content, section_blacklist=None, section_whitelist=None
):
    """wikipedia pages have the following slightly complex schema:

    <div><h2>Section 1 title</h2></div>
    <p>...</p>...
    <div><h2>Section 2 title</h2></div>
    <p>...</p>...
    """
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Adding the intro section, before the first h2 tag
    paragraphs = []
    for element in soup.find_all(["p", "h2"]):
        if element.name == "h2" and element.get_text() != "Contents":
            break
        if element.name == "p":
            paragraphs.append(element.get_text())

    section_data = [{"title": None, "content": " ".join(paragraphs)}]

    # Iterate over each section
    for section in soup.find_all("h2"):
        title = section.get_text(strip=True)  # Extract the title text
        if section_blacklist is not None:
            if title in section_blacklist:
                continue
        if section_whitelist is not None:
            if title not in section_whitelist:
                continue
        content = []  # Initialize content list for this section
        for sibling in section.parent.find_next_siblings():
            if len(sibling.select("h2")):  # Stop if the next h2 section starts
                break
            if sibling.get_text(strip=True):  # Add text content if not empty
                content.append(sibling.get_text())

        # Join the content list into a single string
        content_text = " ".join(content)

        # Append the result as a dictionary
        section_data.append({"title": title, "content": content_text})
    return section_data


def collect_wikipedia_page_and_separate_sections(composer_data):
    composer = composer_data["full_name"]
    wikipedia_url = composer_data["wikipedia_url"]
    html_content = cached_web_request(wikipedia_url)
    section_title_blacklist = [
        "External links",
        "Further reading",
        "Sources",
        "See also",
        "References",
        "Contents",
        "Notes, references and sources",
        "Notes",
        "Notes and references",
        "Recordings",
        "Compositions",
    ]
    sections = _extract_sections_from_wikipedia_page(
        html_content, section_blacklist=section_title_blacklist
    )
    return {"wikipedia_url": wikipedia_url, "sections": sections, "composer": composer}


@gpt_function(retries=2)
def _list_life_events(composer_biography: str, exclude_events: list) -> list[dict]:
    """Return a list the composer's life events from the given text.
    Exclude any event described in the exclude_events list.
    Add the best emoji to describe the event.

    The output should have this schema:
    [{title:str, summary: str, year: int, location: str, emoji: str}...]

    The summary should be a few sentences, and as informative as possible
    but only with information from the text.
    The summary should not state the year.

    Return an empty list if there are no events.
    """


def list_life_events_in_sections(data):
    composer = data["composer"]
    events = []
    for section in data["sections"]:
        title = section["title"]
        text = f"{composer} - {title} - {section['content']}"
        past_events = [f"{e['year']} {e['title']}" for e in events]
        section_events = _list_life_events(
            composer_biography=text, exclude_events=past_events
        )
        events += [{"section": title, **e} for e in section_events]
    return events


@gpt_function(retries=2)
def _most_relevant_emoji(event: str, context: dict) -> dict:
    """Return the most relevant emoji for the given event
    Output schema: {emoji: str}
    """


@gpt_function(retries=2, think_through=True)
def _add_fun_to_text(event_summary: str) -> str:
    """For the given event_summary, follow these steps:

    Step 1: Rewrite the event_summary with humor. Be funny!
    Step 2: Copy the result of Step 1 without any joke about tragic events.
    Step 3: Copy the result of Step 2 without the weakest jokes if the text is over 60 words
    Step 4: Copy the result of Step 3 with any information from the original summary that got lost.
    """


def add_fun_to_events(events):
    events_with_fun = []
    for event in events:
        context = {**event}
        summary = context.pop("summary")
        emoji = _most_relevant_emoji(event_summary=event["summary"], context=context)
        fun_version = _add_fun_to_text(event_summary=summary)
        events_with_fun.append({**event, **emoji, "fun_version": fun_version})
    return events_with_fun


@gpt_function
def _select_major_world_events(text) -> list:
    """Return a list of the top ~10 major events described in the text.

    Prefer major technical advances, or major events which
    would have made the front page of European newspapers.
    Prefer events which could have had an impact on citizens
    and in particular music composers.

    Schema for each event:
    {"title": str, "summary": str, "year": int, "city": str, "country": str}

    The year should always be a single integer, and only an integer.
    Never use quotation marks inside the summary.
    """


def get_world_events(data):
    year = data["year"]
    wikipedia_url = f"https://en.wikipedia.org/wiki/{year}"
    wikipedia_html = cached_web_request(wikipedia_url)
    sections = _extract_sections_from_wikipedia_page(
        wikipedia_html, section_whitelist=["Events"]
    )
    events_txt = sections[0]["content"]
    return _select_major_world_events(text=events_txt)
