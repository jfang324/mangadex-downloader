mock_url: str = "https://test.com"
mock_query: str = "test"
mock_manga_id: str = "1"
mock_chapter_id: str = "1000"

mock_manga_data: dict = {
    "data": [
        {
            "id": "1",
            "attributes": {
                "title": {"en": "Attack on Titan"},
            },
        },
        {
            "id": "2",
            "attributes": {
                "title": {"en": "One Piece"},
            },
        },
        {
            "id": "3",
            "attributes": {
                "title": {"en": "Naruto"},
            },
        },
    ]
}
mock_chapter_data: dict = {
    "data": [
        {
            "id": "1",
            "attributes": {
                "title": "Chapter 1",
                "chapter": "1",
            },
        },
        {
            "id": "2",
            "attributes": {
                "title": "Chapter 2",
                "chapter": "2",
            },
        },
        {
            "id": "3",
            "attributes": {
                "chapter": "3",
            },
        },
        {
            "id": "4",
            "attributes": {
                "title": "Chapter 4",
            },
        },
    ]
}
mock_download_resource_data: dict = {
    "baseUrl": "https://mangaCDN.com/",
    "chapter": {
        "hash": "hash",
        "data": [
            "chapter1.jpg",
            "chapter2.jpg",
            "chapter3.jpg",
            "chapter4.jpg",
        ],
    },
}
mock_image_data: bytes = b"A long string of bytes representing an image"
mock_url_list: list[str] = [
    "https://test.com/1.jpg",
    "https://test.com/2.jpg",
    "https://test.com/3.jpg",
    "https://test.com/4.jpg",
]
