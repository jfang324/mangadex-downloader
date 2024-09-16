import curses


def prompt_user_input(stdscr: curses, message: str) -> str:
    """
    Prompts the user to enter a string

    :param stdscr: The curses object
    :param message: The message to display to the user
    :return: The string entered by the user
    """
    curses.curs_set(1)
    user_input = ""

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"{message}: ", curses.color_pair(1))
        stdscr.addstr(f"{user_input}")
        stdscr.refresh()

        key: str = stdscr.getch()
        if key == ord("\n"):
            break
        elif key == ord("\b"):
            user_input = user_input[:-1]
        elif key == 27:
            user_input = ""
            break
        else:
            if 32 <= key <= 126:
                user_input += chr(key)

    curses.curs_set(0)
    return user_input


def prompt_list_selection(
    stdscr: curses, result_list: list[dict], page_size: int, title: str
) -> int:
    """
    Displays the manga list to the user and prompt them to select a manga

    :param stdscr: The curses object
    :param manga_list: The list of manga to display
    :param page_size: The number of results to display per page
    :param title: The title at the top of the list
    :return: The index of the selected item
    """
    current_index: int = 0

    while True:
        stdscr.clear()
        page_start: int = (current_index // page_size) * page_size
        page_end: int = min(page_start + page_size, len(result_list))

        stdscr.addstr(0, 0, f"{title}:", curses.color_pair(1))
        for i in range(page_start, page_end):
            if i == current_index:
                stdscr.addstr(i - page_start + 1, 0, "> ", curses.color_pair(2))
                stdscr.addstr(
                    f'{i + 1} {result_list[i]["title"]}',
                    curses.A_REVERSE,
                )
            else:
                stdscr.addstr(i - page_start + 1, 0, " ", curses.A_REVERSE)
                stdscr.addstr(" ")
                stdscr.addstr(f'{i + 1} {result_list[i]["title"]}')

        stdscr.addstr(
            f"\n{page_start + 1}-{page_end} of {len(result_list)} results",
            curses.color_pair(1),
        )
        stdscr.refresh()
        key: str = stdscr.getch()

        if key == curses.KEY_UP:
            current_index = max(current_index - 1, 0)
        elif key == curses.KEY_DOWN:
            current_index = min(current_index + 1, len(result_list) - 1)
        elif key == ord("\n"):
            return current_index
        elif key == 27:
            return -1
        else:
            continue
