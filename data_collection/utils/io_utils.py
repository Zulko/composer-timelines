from pathlib import Path
import json
import time
import asyncio

from fastprogress import progress_bar
import requests
import aiohttp

from aiohttp_client_cache import CachedSession, SQLiteBackend

cache_path = Path(__file__).parent / "web-cache"
cache = SQLiteBackend(cache_name=cache_path)



async def cached_web_request(url, params=None, response_type="html", sleep_after=0):
    requests_cache_session = CachedSession(cache=cache)
    try:
        async with requests_cache_session as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                await asyncio.sleep(sleep_after)
                if response_type == "json":
                    return await response.json()
                elif response_type == "html":
                    return await response.text()
    except aiohttp.ClientError as e:
        print(f"Failed to download {url}: {e}")


def save_to_json(data, filepath):
    json.dump(data, open(filepath, "w"), indent=2)


def load_from_json(filepath):
    return json.load(open(filepath, "r"))


async def process_folder(
    function, source_folder, target_folder, replace_existing=False, concurrency=10
):
    source_folder = Path(source_folder)
    source_files = list(source_folder.glob("*"))

    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    if not replace_existing:
        already_processed = {f.stem for f in target_folder.glob("*")}
        source_files = [f for f in source_files if f.stem not in already_processed]

    async def process_file(file):
        data = load_from_json(file)
        result = await function(data)  # Assuming function is now async
        save_to_json(result, target_folder / file.name)

    semaphore = asyncio.Semaphore(concurrency)

    async def bounded_process_file(file):
        async with semaphore:
            await process_file(file)

    tasks = [bounded_process_file(file) for file in source_files]
    
    for task in progress_bar(asyncio.as_completed(tasks), total=len(tasks)):
        await task