from pathlib import Path
import multiprocessing
import json
import time
from fastprogress import progress_bar
import requests_cache
import requests

cache_path = Path(__file__).parent / "web-cache"
requests_cache_session = requests_cache.CachedSession(cache_path)


def cached_web_request(url, params=None, response_type="html", sleep_after=0):
    try:
        response = requests_cache_session.get(url, params=params)
        response.raise_for_status()
        time.sleep(sleep_after)
        if response_type == "json":
            return response.json()
        elif response_type == "html":
            return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


def save_to_json(data, filepath):
    json.dump(data, open(filepath, "w"), indent=2)


def load_from_json(filepath):
    return json.load(open(filepath, "r"))


def _run_function_on_file(args):
    function, source, target = args
    data = load_from_json(source)
    result = function(data)
    save_to_json(result, target)


def process_folder(
    function, source_folder, target_folder, replace_existing=False, num_processes=1
):
    source_folder = Path(source_folder)
    source_files = list(source_folder.glob("*"))

    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    if not replace_existing:
        already_processed = {f.stem for f in target_folder.glob("*")}
        source_files = [f for f in source_files if f.stem not in already_processed]

    if (len(source_files) > 1) and (num_processes > 1):
        with multiprocessing.Pool(processes=num_processes) as pool:
            args = [
                (function, file, target_folder / file.name) for file in source_files
            ]
            pooled = pool.imap(_run_function_on_file, args)
            for _i in progress_bar(pooled, total=len(source_files)):
                pass

    else:
        for file in progress_bar(source_files):
            _run_function_on_file((function, file, target_folder / file.name))
