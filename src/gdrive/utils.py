import logging
import os
import zipfile

import gdown


def download(id: str, output: str):
    """
    fetches a GDrive file from id, extracts results and deletes temp file
    """
    if os.path.exists(output) and os.listdir(output) != [".gitkeep"]:
        logging.info(f"aborting download as folder {output} already contains data")
        return

    temp_file = output + ".zip"
    url = f"https://drive.google.com/uc?id={id}"

    logging.info(f"downloading zip file {temp_file} from {url}")
    gdown.download(url, temp_file, quiet=False)

    logging.info(f"extracting {temp_file} to {output}")
    with zipfile.ZipFile(temp_file, "r") as zip_ref:
        zip_ref.extractall(output)

    logging.info(f"removing temp file {temp_file}")
    os.remove(temp_file)
