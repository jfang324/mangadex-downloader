## About The Project

A CLI tool that makes it easy to search for and download manga from [MangaDex](https://mangadex.org/)

## Getting Started

### Prerequisites

To use this tool, you will need the following:

-   Python 3.11 or higher
-   python-dotenv (if you want to use the .env file, optional unless the API changes)
-   aiohttp
-   Pillow
-   windows-curses (if you are using Windows)

To run the tests, you will need the following:

-   Pytest
-   Coverage

## Installation

To install the tool, run the following commands in your terminal:

1. Clone the repository:

```bash
git clone https://github.com/jfang324/mangadex-downloader.git
```

2. Navigate to the project directory:

```bash
cd mangadex-downloader
```

3. If using Windows, install the windows-curses package:

```bash
pip install windows-curses
```

4. Install the project using pip:

```bash
pip install .
```

5. The script will now be installed in your python scripts directory where you can run it or add it to your PATH to be able to run it from anywhere.

## Gallery & Demonstrations

## Acknowledgements

-   [MangaDex](https://mangadex.org/) for providing the API used in this project

## Known Issues

-   Characters that can't be used in file names cause unexpected behavior when generating the PDF file when they are included in the title of the manga
-   Characters used for query parameters cause unexpected behavior included in user input

## Contact

Jeffery Fang - [jefferyfang324@gmail.com](mailto:jefferyfang324@gmail.com)

## Tools & Technologies

-   Python
-   Curses/Windows-Curses
-   aiohttp
-   Pillow
-   Pytest
-   Coverage
-   Poetry
