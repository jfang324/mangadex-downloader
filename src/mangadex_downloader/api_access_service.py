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


async def retrieve_download_resources(chapter_id: str) -> dict:
    """
    Query MangaDex API for download resources of the chapter with the given chapter_id

    :param chapter_id: The id of the chapter to retrieve download resources for
    :return: A dictionary containing information for download resources of the chapter
    """
    try:
        url: str = f"{mangadex_resource_links_url}/{chapter_id}"

        return await fetch_url(url)
    except Exception as e:
        print(e)
        return None


async def retrieve_image_data(image_url: str) -> bytes:
    """
    Retrives the image data from the given image url

    :param image_url: The url of the image to retrieve data for
    :return: The binary data of the image
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                return await response.read()
            else:
                raise Exception(
                    f"Failed to retrieve image data for {image_url}. Status code: {response.status}"
                )


async def retrieve_image_data_list(url_list: list[str]) -> list[bytes]:
    """
    Retrives the image data from the given image urls

    :param image_links: The urls of the images to retrieve data for
    :return: A list containing the binary data of the images
    """

    async with aiohttp.ClientSession() as session:
        tasks = [retrieve_image_data(url) for url in url_list]

    return await asyncio.gather(*tasks)
