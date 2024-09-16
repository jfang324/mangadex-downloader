import os
import tempfile
from PIL import Image


def save_image(image_data: bytes, file_path: str) -> None:
    """
    Saves the image data to a file with the given file name

    :param image_data: The image data to save
    :param file_name: The file name to save the image data as
    :return: None
    """

    if image_data:
        with open(file_path, "wb") as file:
            file.write(image_data)


def save_image_list(image_data_list: list[bytes], directory: str) -> None:
    """
    Saves each element in the image data list to a file named after the index of the element

    :param image_data_list: The image data list to save
    :return: None
    """

    for i, image_data in enumerate(image_data_list):
        file_path: str = os.path.join(directory, f"{i}.jpg")
        save_image(image_data, file_path)


def get_file_list(path: str) -> list[str]:
    """
    Get a list of all files in a directory.

    :param path: The path to the directory.
    :return: A list of all files in the directory.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"The directory {path} does not exist.")

        if os.path.isfile(path):
            raise Exception(f"{path} is not a directory.")

        everything_list: list[str] = os.listdir(path)
        file_list: list[str] = []

        for item in everything_list:
            if os.path.isfile(os.path.join(path, item)) and item.endswith(
                (".png", ".jpg", ".jpeg")
            ):
                file_list.append(os.path.join(path, item))

        return file_list
    except Exception as e:
        print(e)
        return []


def convert_images_to_pdf(
    file_list: list[str], output_path: str, output_name: str
) -> None:
    """
    Converts a list of images to a PDF file.

    :param file_list: A list of image files to be converted.
    :param output_path: The path to the output directory.
    :param output_name: The name of the output PDF file.
    """
    images: Image.Image = [
        Image.open(file)
        for file in file_list
        if os.path.exists(file) and os.path.isfile(file)
    ]
    images[0].save(
        os.path.join(output_path, output_name + ".pdf"),
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=images[1:],
    )


def generate_PDF(image_data_list: list[bytes], output_name: str) -> None:
    """
    Generates a PDF file from the image data list by creating a temporary directory and saving each image to a file
    in the temporary directory, then converting the temporary directory to a PDF file

    :param image_data_list: The image data list to convert to a PDF file
    :param output_name: The name of the output PDF file
    :return: None
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Generating {output_name}.pdf...")
        save_image_list(image_data_list, temp_dir)
        convert_images_to_pdf(get_file_list(temp_dir), os.getcwd(), output_name)
