def process_manga_data(manga_data: dict) -> list[dict]:
    """
    Processes the manga_data dictionary to contain only the following fields:
    {
        title: title of the manga,
        id: mangaID for the API
    }

    :param manga_data: The manga data dictionary
    :return: A list containing the processed manga data
    """

    processed_manga_data: list[dict] = []
    data: list[dict] = manga_data["data"]

    for element in data:
        if "id" in element:
            manga = {}
            manga["title"] = (
                element["attributes"]["title"]["en"]
                if "title" in element["attributes"]
                and "en" in element["attributes"]["title"]
                else element["attributes"]["title"][
                    list(element["attributes"]["title"])[0]
                ]
            )
            manga["id"] = element["id"]
            processed_manga_data.append(manga)

    return processed_manga_data


def process_chapter_data(chapter_data: dict) -> list[dict]:
    """
    Processes the chapter_data dictionary to contain only the following fields:
    {
        title: title of the chapter,
        id: chapterID for the API,
        chapter_number: chapter number
    }

    :param chapter_data: The chapter data dictionary
    :return: A list containing the processed chapter data
    """

    processed_chapter_data: list[dict] = []
    data: list[dict] = chapter_data["data"]
    already_contains: set[str] = set()

    for element in data:
        if "id" in element:
            chapter = {}
            chapter["title"] = (
                element["attributes"]["title"]
                if "title" in element["attributes"]
                else None
            )
            chapter["id"] = element["id"]
            chapter["chapter_number"] = (
                element["attributes"]["chapter"]
                if "chapter" in element["attributes"]
                and element["attributes"]["chapter"]
                else "0"
            )

            if chapter["chapter_number"] not in already_contains:
                already_contains.add(chapter["chapter_number"])
                processed_chapter_data.append(chapter)

    processed_chapter_data.sort(key=lambda x: float(x["chapter_number"]))

    return processed_chapter_data


def process_download_resource_data(download_resources: dict) -> list[str]:
    """
    Processes the download_resources dictionary into a list of download urls

    :param download_resources: The download resources data dictionary
    :return: A list containing the download urls
    """

    download_urls: list[str] = []
    base_url: str = download_resources["baseUrl"]
    url_hash: str = download_resources["chapter"]["hash"]
    quality: str = "data"

    for element in download_resources["chapter"][quality]:
        download_urls.append(f"{base_url}/{quality}/{url_hash}/{element}")

    return download_urls
