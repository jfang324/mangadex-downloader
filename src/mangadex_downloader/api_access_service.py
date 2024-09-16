from dotenv import load_dotenv
import os
import asyncio
import aiohttp

load_dotenv()

mangadex_root_url: str = os.getenv("MANGADEX_ROOT_URL")
mangadex_resource_links_url: str = os.getenv("MANGADEX_RESOURCE_LINKS_URL")


async def fetch_url(url: str, params: dict = {}) -> dict:
    """
    Makes a GET request to the url and returns the response

    :param url: The url to fetch
    :return: The response from the url
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Error fetching url: {response.status}")


async def retrieve_mangas(query: str) -> dict:
    """
    Query MangaDex API for manga's similiar to the query

    :param query: The query to search for
    :return: A dictionary containing information for similiar mangas
    """
    try:
        url: str = f"{mangadex_root_url}?title={query}"
        params: dict = {"limit": 100}

        return await fetch_url(url, params=params)
    except Exception as e:
        print(e)
        return None


async def retrieve_chapters(manga_id: str) -> dict:
    """
    Query MangaDex API for chapters of the manga with the given manga_id

    :param manga_id: The id of the manga to retrieve chapters for
    :return: A dictionary containing information for chapters of the manga
    """
    try:
        url: str = f"{mangadex_root_url}/{manga_id}/feed"
        params: dict = {
            "translatedLanguage[]": ["en"],
            "limit": 500,
            "includeEmptyPages": 0,
        }

        return await fetch_url(url, params)
    except Exception as e:
        print(e)
        return None
