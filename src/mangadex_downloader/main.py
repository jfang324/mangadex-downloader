import asyncio
import curses
from .api_access_service import *
from .data_processing_service import *
from .user_interface_service import *
from .file_access_services import *


async def start(stdscr: curses) -> None:
    # Main body of the program

    # Initialize curses settings for UI
    curses.curs_set(0)
    curses.noecho()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    # Prompt user for a initial query
    query: str = prompt_user_input(stdscr, "Enter a manga title")

    # Exit if no input was given
    if query == "":
        return

    # Retrieve and process the API response into a list of mangas similar to the query
    manga_data: dict = await retrieve_mangas(query)
    processed_manga_data: list[dict] = process_manga_data(manga_data)

    # Prompt user to select a manga out of the list of mangas
    selected_manga_index: int = prompt_list_selection(
        stdscr, processed_manga_data, 20, "Select manga"
    )

    # Exit if no manga was selected
    if selected_manga_index == -1:
        return

    # Retrieve and process the API response into a list of chapters of the selected manga
    chapter_data: dict = await retrieve_chapters(
        processed_manga_data[int(selected_manga_index)]["id"]
    )
    processed_chapter_data: list[dict] = process_chapter_data(chapter_data)

    # Prompt user to select a chapter out of the list of chapters
    selected_chapter_index: int = prompt_list_selection(
        stdscr, processed_chapter_data, 20, "Select chapter"
    )

    # Exit if no chapter was selected
    if selected_chapter_index == -1:
        return

    # Retrieve and process the API response into a list of download links for the selected chapter
    download_resources: dict = await retrieve_download_resources(
        processed_chapter_data[int(selected_chapter_index)]["id"]
    )
    download_links: list[str] = process_download_resource_data(download_resources)

    # Download the images from the download links and generate a PDF file
    image_data_list: list[bytes] = await retrieve_image_data_list(download_links)
    generate_PDF(
        image_data_list,
        f'{processed_manga_data[int(selected_manga_index)]["title"]} [{processed_chapter_data[int(selected_chapter_index)]["chapter_number"]}]',
    )


def curses_main(stdscr: curses) -> None:
    # Run the start function in an asyncio.run to enable use of async/await
    asyncio.run(start(stdscr))


def main():
    # wrap curses_main in curses.wrapper to initialize curses
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
