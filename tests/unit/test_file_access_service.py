import os
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from mangadex_downloader.services.file_access_service import *
from tests.mock_data import *


def create_mock_file() -> MagicMock:
    mock_file: MagicMock = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.write.return_value = None

    return mock_file


class TestSaveImage:
    @patch("builtins.open", new_callable=create_mock_file)
    def test_save_image_writes_bytes_to_file(self, mock_open: MagicMock):
        image_data: bytes = mock_image_data_list[0]
        file_path: str = mock_image_paths[0]

        save_image(image_data, file_path)
        mock_open.assert_called_once_with(file_path, "wb")
        mock_open().__enter__().write.assert_called_once_with(image_data)

    @patch("builtins.open", new_callable=create_mock_file)
    def test_save_image_does_not_write_bytes_to_file_if_image_data_is_none(
        self, mock_open: MagicMock
    ):
        image_data: bytes = None
        file_path: str = mock_image_paths[0]

        save_image(image_data, file_path)
        mock_open.assert_not_called()


class TestSaveImageList:
    @patch("mangadex_downloader.services.file_access_service.save_image")
    def test_save_image_list_saves_each_image_in_image_data_list_to_a_file(
        self, mock_save_image: MagicMock
    ):
        image_data_list: list[bytes] = mock_image_data_list
        directory: str = mock_directory

        save_image_list(image_data_list, directory)
        for i, image_data in enumerate(image_data_list):
            assert mock_save_image.call_args_list[i][0][0] == image_data
            assert mock_save_image.call_args_list[i][0][1] == os.path.join(
                directory, f"{i}.jpg"
            )


class TestGetFileList:
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile")
    @patch("os.listdir", return_value=mock_image_paths)
    def test_get_file_list_returns_correct_file_list(
        self, mock_listdir: MagicMock, mock_isfile: MagicMock, mock_exists: MagicMock
    ):
        isfile_list = [False]
        isfile_list.extend([True] * len(mock_image_paths))
        mock_isfile.side_effect = isfile_list
        response: list[str] = get_file_list(mock_directory)

        assert response == [
            os.path.join(mock_directory, path) for path in mock_image_paths
        ]

    @patch("os.path.exists", return_value=False)
    def test_get_file_list_returns_empty_list_if_directory_does_not_exist(
        self, mock_exists: MagicMock
    ):
        response: list[str] = get_file_list(mock_directory)

        assert response == []

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    def test_get_file_list_returns_empty_list_if_directory_is_not_a_directory(
        self, mock_isfile: MagicMock, mock_exists: MagicMock
    ):
        response: list[str] = get_file_list(mock_directory)

        assert response == []

    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile")
    @patch("os.listdir")
    def test_get_file_list_ignores_files_that_are_not_images(
        self, mock_listdir: MagicMock, mock_isfile: MagicMock, mock_exists: MagicMock
    ):
        dir_list = ["file1.txt", "file2.pdf"]
        dir_list.extend(mock_image_paths)
        mock_listdir.return_value = dir_list

        isfile_list = [False]
        isfile_list.extend([True] * len(dir_list))
        mock_isfile.side_effect = isfile_list

        response: list[str] = get_file_list(mock_directory)

        assert response == [
            os.path.join(mock_directory, path) for path in mock_image_paths
        ]


class TestConvertImagesToPDF:
    @patch("os.path.exists", return_value=True)
    @patch("os.path.isfile", return_value=True)
    @patch("PIL.Image.open", return_value=Image.new("RGB", (100, 100)))
    @patch("PIL.Image.Image.save", return_value=None)
    @patch("os.path.join", return_value="/path/to/output.pdf")
    def test_convert_images_to_pdf_with_valid_file_list_and_output_path_and_name(
        self,
        mock_join: MagicMock,
        mock_save: MagicMock,
        mock_open: MagicMock,
        mock_isfile: MagicMock,
        mock_exists: MagicMock,
    ):
        output_path: str = "/path/to/output"
        output_name: str = "output"
        convert_images_to_pdf(mock_image_paths, output_path, output_name)

        for file in mock_image_paths:
            mock_open.assert_any_call(file)

        mock_save.assert_called_once_with(
            os.path.join(output_path, output_name + ".pdf"),
            "PDF",
            save_all=True,
            append_images=[
                Image.new("RGB", (100, 100)) for i in range(len(mock_image_paths))
            ][1:],
        )

    @patch("os.path.exists")
    @patch("os.path.isfile", return_value=True)
    @patch("PIL.Image.open", return_value=Image.new("RGB", (100, 100)))
    @patch("PIL.Image.Image.save", return_value=None)
    @patch("os.path.join", return_value="/path/to/output.pdf")
    def test_convert_images_to_pdf_with_invalid_files_in_file_list_ignores_them(
        self,
        mock_join: MagicMock,
        mock_save: MagicMock,
        mock_open: MagicMock,
        mock_isfile: MagicMock,
        mock_exists: MagicMock,
    ):
        output_path: str = "/path/to/output"
        output_name: str = "output"
        exists_list = [False]
        exists_list.extend([True] * len(mock_image_paths))
        mock_exists.side_effect = exists_list
        convert_images_to_pdf(mock_image_paths, output_path, output_name)

        assert mock_open.call_count == len(mock_image_paths) - 1
        mock_save.assert_called_once_with(
            os.path.join(output_path, output_name + ".pdf"),
            "PDF",
            save_all=True,
            append_images=[
                Image.new("RGB", (100, 100)) for i in range(len(mock_image_paths) - 1)
            ][1:],
        )
