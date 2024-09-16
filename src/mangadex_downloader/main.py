import asyncio
import curses
from .api_access_service import *
from .data_processing_service import *
from .user_interface_service import *
from .file_access_services import *


async def start(stdscr: curses) -> None:
    curses.curs_set(0)
    curses.start_color()
    curses.noecho()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    query: str = prompt_user_input(stdscr, "Enter a manga title")

    if query == "":
        return

    manga_data: dict = await retrieve_mangas(query)
    proccessed_manga_data: list[dict] = process_manga_data(manga_data)

    selected_manga_index: int = prompt_list_selection(
        stdscr, proccessed_manga_data, 20, "Select manga"
    )

    if selected_manga_index == -1:
        return

    chapter_data: dict = await retrieve_chapters(
        proccessed_manga_data[int(selected_manga_index)]["id"]
    )
    proccessed_chapter_data: list[dict] = process_chapter_data(chapter_data)

    selected_chapter_index: int = prompt_list_selection(
        stdscr, proccessed_chapter_data, 20, "Select chapter"
    )

    if selected_chapter_index == -1:
        return

    download_resources: dict = await retrieve_download_resources(
        proccessed_chapter_data[int(selected_chapter_index)]["id"]
    )
    download_links: list[str] = process_download_resource_data(download_resources)
    image_data_list: list[bytes] = await retrieve_image_data_list(download_links)
    generate_PDF(
        image_data_list,
        f'{proccessed_manga_data[int(selected_manga_index)]["title"]} [{proccessed_chapter_data[int(selected_chapter_index)]["chapter_number"]}]',
    )


def curses_main(stdscr: curses) -> None:
    asyncio.run(start(stdscr))


def main():
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
