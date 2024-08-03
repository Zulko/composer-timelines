"""
Usage:
  add_composer.py --composer=<name> --target=<path>

Options:
  -h --help     Show this screen.
"""

from pathlib import Path
from docopt import docopt
import utils
import logging

logging.basicConfig(level=logging.INFO)


def add_composer(composer_name, target_folder):

    target_folder = Path(target_folder)
    composer_list = target_folder / "composers.json"
    composers = utils.load_from_json(composer_list)

    logging.info(f"Searching for {composer_name} on wikipedia...")
    metadata = utils.get_basic_metadata_from_wikipedia({"name": composer_name})
    full_name = metadata["full_name"]

    if full_name in [c["full_name"] for c in composers]:
        logging.info(f"{full_name} already in the list.")
        return

    birth, death = metadata["birth_year"], metadata["death_year"]
    logging.info(f"Basic info found from wikipedia: {metadata}")

    data = {**metadata}

    logging.info("Summarizing events in wikipedia page...")
    wikipedia_sections = utils.collect_wikipedia_page_and_separate_sections(metadata)
    events = utils.list_life_events_in_sections(wikipedia_sections)
    events = [e for e in events if e["year"] and (birth <= e["year"] <= death)]

    logging.info("Adding fun to the events...")
    events = utils.add_fun_to_events(events)
    if min([e["year"] for e in events]) != birth:
        events.append({"year": birth, "title": "Birth"})
    if max([e["year"] for e in events]) != death:
        events.append({"year": death, "title": "Death"})
    data["events"] = sorted(events, key=lambda e: (e["year"], e["title"]))

    logging.info("Getting works from IMSLP...")
    works = utils.get_works_data_from_imslp(metadata)
    works = [w for w in works if w["year"] and (birth <= w["year"] <= death)]
    data["works"] = sorted(works, key=lambda w: (w["year"], w["title"]))

    logging.info(f"Collected {len(events)} events {len(works)} and works.")

    # Save data to disk

    target_file = target_folder / "composer_data" / f"{full_name}.json"
    utils.save_to_json(data, target_file)

    composers.append(metadata)
    composers = sorted(composers, key=lambda c: c["last_name"])
    utils.save_to_json(composers, composer_list)


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Composer Script 1.0")
    add_composer(arguments["--composer"], arguments["--target"])
