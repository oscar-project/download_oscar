import argparse
import os
from hashlib import sha256
from io import StringIO
from pathlib import Path
from typing import List

import requests
from bs4 import BeautifulSoup
from requests import sessions
from tqdm import tqdm

from download_oscar.status import Status


def login(user: str, password: str, s: sessions.Session, headers):
    """Logs in to the base website of the oscar dataset.

    Args:
        user (str): User name of the account to login to.
        password (str): Password for the user.
        s (sessions.Session): The session that should be used to login.
        headers (): The headers used in requests.
    """

    login_url = "https://humanid.huma-num.fr/"
    login_data = {
        "user": user,
        "password": password,
        "timezone": "1",
        "lmAuth": "1HumanID",
        "skin": "humanid",
    }
    response = s.get(login_url, headers=headers)

    soup = BeautifulSoup(response.content, "html5lib")

    login_data["url"] = (soup.find("input", attrs={"name": "url"})["value"],)
    login_data["token"] = (soup.find("input", attrs={"name": "token"})["value"],)

    response = s.post(login_url, headers=headers, data=login_data)


def get_filename(url: str) -> str:
    """Returns the filename from a link.

    Args:
        url (str): The url to a file location on the website.

    Returns:
        str: Only the filename.
    """
    return url.split("/")[-1]


def validate_file(checksum: str, filename: str) -> bool:
    """Checks if the checksum is equal to the sha256 hex of the file, if it exists.

    Args:
        checksum (str): The checksum the file needs to satisfy.
        filename (str): The filename of the file to check.

    Returns:
        bool: The result of the comparison of the checksum and the file.
    """
    if not Path(filename).is_file():
        return False

    hash_value = sha256()
    with open(filename, "rb") as file:
        while True:
            chunk = file.read(hash_value.block_size)
            if not chunk:
                break
            hash_value.update(chunk)
    return hash_value.hexdigest() == checksum


def file_exists(filename: str, checksum: str) -> bool:
    """Checks if a file already exists.

    Args:
        filename (str): The filename to check.
        checksum (str): The checksum the file must correspond to.

    Returns:
        bool: The result of the check.
    """
    return validate_file(checksum, filename)


def download_data(
    s: sessions.Session,
    data_url: str,
    chunk_size: int,
    checksum: str,
    out: str,
    headers,
) -> Status:
    """Downloads a data file using streaming and validates that downloaded file corresponds to the checksum.
    Files are not downloaded again if already present.

    Args:
        s (sessions.Session): The session used to login to the website.
        data_url (str): The url of the file to download.
        chunk_size (int): Specifies the size in how files should be streamed.
        checksum (str): The checksum the downloaded file must correspond to.
        headers (): The headers used in requests.

    Returns:
        Status: The status of the downloaded result.
    """
    os.makedirs(Path(out), exist_ok=True)
    out_file = os.path.join(out, get_filename(data_url))
    if file_exists(out_file, checksum):
        return Status.EXISTS, out_file
    download = s.get(data_url, stream=True, headers=headers)
    download.raise_for_status()

    if download.status_code != 200:
        return Status.DOWNLOAD_FAILED, out_file

    try:
        with open(out_file, "wb") as f:
            with tqdm(
                total=int(download.headers.get("content-length", 0)),
                desc=out_file,
                miniters=1,
                unit_scale=True,
                unit_divisor=1024,
                unit="B",
                position=2,
            ) as progress_bar:
                for chunk in download.iter_content(chunk_size=chunk_size):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        progress_bar.update(len(chunk))
    except Exception:
        return Status.DOWNLOAD_FAILED, out_file

    if validate_file(checksum, out_file):
        return Status.DOWNLOAD_SUCCESS, out_file
    return Status.VALIDATION_FAILED, out_file


def download_checksums(s: sessions.Session, checksum_url: str, headers) -> dict:
    """Downloads the checksum file and creates a dictionary where the key is the filename and value is the corresponding checksum.

    Args:
        s (sessions.Session): The session used to login before downloading.
        checksum_url (str): The url to download the checksum file.
        headers (): The headers used in requests.

    Returns:
        dict: Filenames with corresponding checksum.
    """
    download = s.get(checksum_url, headers=headers)
    download.raise_for_status()

    with StringIO(download.text) as buffer:
        lines = buffer.readlines()
        dictionary = {}
        for line in lines:
            (key, val) = line.split()
            dictionary[key] = val
        return dictionary


def download_all(user: str, password: str, base_url: str, out, chunk_size: int = 4096):
    """Download all data files from the base_url.

    Args:
        user (str): The user name needed to login to the base_url.
        password (str): The password for this username.
        base_url (str): The base_url where all data files for a language can be found.
        chunk_size (int, optional): Specifies that downloads should be downloaded in parts of this size. Defaults to 4096.
    """
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.41 Safari/537.36"
    }
    with requests.session() as session:
        login(user, password, session, headers)

        response = session.get(base_url, headers=headers)

        checksums_url = get_checksums_location(base_url, response.content)
        checksums = download_checksums(session, checksums_url, headers)

        results = {}
        try:
            for data_url in tqdm(
                get_unique_file_locations(base_url, response.content),
                desc="Files: ",
                position=1,
            ):
                (status, filename) = download_data(
                    session,
                    data_url,
                    chunk_size,
                    checksums[get_filename(data_url)],
                    out,
                    headers,
                )
                results[filename] = status
        finally:
            os.makedirs(out, exist_ok=True)
            with open(os.path.join(out, "results.txt"), "w") as file:
                print(results, file=file)


def get_unique_file_locations(base_url: str, response_content: bytes) -> List[str]:
    """Returns the unique links to the locations of data files with respect to the base url.

    Args:
        base_url (str): The base url for the language to download.
        response_content (bytes): The content of the response which logged in to the base_url.

    Returns:
        List[str]: The unique links for all data files.
    """
    soup = BeautifulSoup(response_content, "html5lib")
    return list(
        set(
            [
                "/".join([base_url, link["href"]])
                for link in soup.find_all("a", href=True)
                if "txt.gz" in link["href"]
            ]
        )
    )


def get_checksums_location(base_url: str, response_content: bytes) -> str:
    """Generates the href to the checksum file.

    Args:
        base_url (str): The base url for the language to download.
        response_content (bytes): The content of the response which logged in to the base_url.

    Returns:
        str: The link for the checksum file.
    """
    soup = BeautifulSoup(response_content, "html5lib")
    checksum_file = [
        "/".join([base_url, link["href"]])
        for link in soup.find_all("a", href=True)
        if "sha256.txt" in link["href"]
    ][0]
    return checksum_file


def main():
    """Download all data files from the base_url."""
    parser = argparse.ArgumentParser(
        prog="download_oscarcorpus",
        description="Download all data files from a given base url.",
    )
    parser.add_argument(
        "--user", action="store", type=str, required=True, help="The login username."
    )
    parser.add_argument(
        "--password",
        action="store",
        type=str,
        required=True,
        help="The login password.",
    )
    parser.add_argument(
        "--base_url",
        action="store",
        type=str,
        required=True,
        help="The base url to download files from.",
    )
    parser.add_argument(
        "--out",
        action="store",
        type=str,
        required=True,
        help="The folder where downloaded files should be saved to.",
    )
    parser.add_argument(
        "--chunk_size",
        action="store",
        type=int,
        default=4096,
        help="Specifies in which chunks downloads are to be processed.",
    )

    args = parser.parse_args()

    download_all(args.user, args.password, args.base_url, args.out, args.chunk_size)


if __name__ == "__main__":
    main()
