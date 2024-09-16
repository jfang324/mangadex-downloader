import asyncio
import curses
from .api_access_service import *
from .data_processing_service import *
from .user_interface_service import *


async def start(stdscr: curses) -> None:
    cursor_index: int = 0
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
        stdscr, proccessed_manga_data, 10, "Select manga"
    )

    if selected_manga_index == -1:
        return

    chapter_data: dict = await retrieve_chapters(
        proccessed_manga_data[int(selected_manga_index)]["id"]
    )
    proccessed_chapter_data: list[dict] = process_chapters(chapter_data)

    selected_chapter_index: int = prompt_list_selection(
        stdscr, proccessed_chapter_data, 20, "Select chapter"
    )

    if selected_chapter_index == -1:
        return

    print(query)
    print(selected_manga_index)
    print(selected_chapter_index)


def curses_main(stdscr: curses) -> None:
    asyncio.run(start(stdscr))


def main():
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
