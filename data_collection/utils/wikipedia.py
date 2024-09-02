import asyncio

from gpt_function_decorator import gpt_function
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup

from .io_utils import cached_web_request


async def _get_wikipedia_url_from_search(term):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {"action": "query", "list": "search", "srsearch": term, "format": "json"}

    data = await cached_web_request(search_url, params=params, response_type="json")

    if data["query"]["search"]:
        title = data["query"]["search"][0]["title"]
        page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
        return page_url
    else:
        print(f"No page found for {term}")
        return None


class Composer(BaseModel):
    first_names: str
    last_name: str
    birth_year: int
    death_year: int


@gpt_function
async def composer_metadata(composer: str, info: str) -> Composer:
    """Return data on {composer}, using the provided info."""


async def get_basic_metadata_from_wikipedia(composer_data):
    wikipedia_url = await _get_wikipedia_url_from_search(composer_data["name"])
    wikipedia_html = await cached_web_request(wikipedia_url)
    soup = BeautifulSoup(wikipedia_html, "html.parser")
    composer_name = soup.select_one("h1").get_text()
    content = soup.select("#bodyContent")[0]
    first_paragraphs = [p.text.strip() for p in content.find_all("p")[:3]]
    metadata = await composer_metadata(composer_name, info=" ".join(first_paragraphs))
    return {
        "full_name": composer_name,
        "wikipedia_url": wikipedia_url,
        **metadata.dict(),
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


async def collect_wikipedia_page_and_separate_sections(composer_data):
    composer = composer_data["full_name"]
    wikipedia_url = composer_data["wikipedia_url"]
    html_content = await cached_web_request(wikipedia_url)
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


class LifeEvent(BaseModel):
    title: str
    summary: str = Field(
        description="A few sentences summarizing the event, as informative as possible "
        "but only with information from the biography. Doesn't state the year."
    )
    year: int
    location: str
    emoji: str


@gpt_function
async def _list_life_events(
    composer_biography: str, exclude_events: list[str]
) -> list[LifeEvent]:
    """List the composer's life events from the composer biography, excluding any event
    described in exclude_events. Return an empty list if there are no events.
    """


async def list_life_events_in_sections(data):
    """List the composer's life events from the composer biography, excluding any event
    described in exclude_events. Return an empty list if there are no events.
    """
    composer = data["composer"]
    events = []
    for section in data["sections"]:
        title = section["title"]
        text = f"{composer} - {title} - {section['content']}"
        past_events = [f"{e['year']} {e['title']}" for e in events]
        section_events = await _list_life_events(
            composer_biography=text, exclude_events=past_events
        )
        events += [{"section": title, **e.dict()} for e in section_events]
    return events


@gpt_function(reasoning=True)
async def _most_relevant_emoji(event: str, context: dict) -> str:
    """Return the most relevant emoji for the given event"""


@gpt_function(reasoning=True)
async def _add_fun_to_text(event_summary: str) -> str:
    """Starting from this summary "{event_summary}", follow these steps:

    Step 1: Rewrite the summary with humor. Be funny!
    Step 2: Copy the result of Step 1 without any joke about tragic events.
    Step 3: Copy the result of Step 2 without the weakest jokes if the text is over 60 words
    Step 4: Copy the result of Step 3 with any information from the original summary that got lost.
    Return the result of Step 4
    """


async def add_fun_to_event(event):
    context = {**event}
    summary = context.pop("summary")
    emoji = _most_relevant_emoji(event=summary, context=context)
    fun_version = _add_fun_to_text(event_summary=summary)
    return {**event, "emoji": await emoji, "fun_version": await fun_version}


async def add_fun_to_events(events):
    return await asyncio.gather(*[add_fun_to_event(event) for event in events])


class WorldEvent(BaseModel):
    title: str
    summary: str
    year: int
    city: str
    country: str


@gpt_function
async def _select_major_world_events(text) -> list[WorldEvent]:
    """Return a list of the top ~10 major events described in the text.

    Prefer major technical advances, or major events which
    would have made the front page of European newspapers.
    Prefer events which could have had an impact on citizens
    and in particular music composers.
    """


async def get_world_events(year_data) -> list[WorldEvent]:
    # The year is provided as a dict as it will be read from JSON via our
    # standardized `process_folder` function
    year = year_data["year"]
    wikipedia_url = f"https://en.wikipedia.org/wiki/{year}"
    wikipedia_html = await cached_web_request(wikipedia_url)
    sections = _extract_sections_from_wikipedia_page(
        wikipedia_html, section_whitelist=["Events"]
    )
    events_txt = sections[0]["content"]
    return await _select_major_world_events(text=events_txt)
