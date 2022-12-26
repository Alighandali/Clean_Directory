import json
import shutil
import sys
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR


class OrganizeFiles:
    """
    This class is used to organize files in a directory by
    moving files into sub-directories based on extention.
    """
    def __init__(self):
        with open(DATA_DIR / 'extentions.txt') as f:
            ext_dirs = json.load(f)
        self.extentions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extentions_dest[ext] = dir_name

    def __call__(self, directory: Union[str, Path]):
        """Organize files in a directry by moving them
        to sub directories based on extention.
        :param directory: path of directory to get organized
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f'{directory} does not exist')
        logger.info(f'Organizing files in {directory}...')
        file_extentions = []
        self.file_counter = 0
        for file_path in directory.iterdir():
            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # move files
            file_extentions.append(file_path.suffix)
            if file_path.suffix not in self.extentions_dest:
                DEST_DIR = directory / 'other'
            else:
                DEST_DIR = directory / self.extentions_dest[file_path.suffix]
            self.file_counter += 1
            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'moving {file_path} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == '__main__':
    org_files = OrganizeFiles()
    org_files(sys.argv[1])
    logger.info(f'{org_files.file_counter} Files Got Organized!')
    print('***************Done***************')
