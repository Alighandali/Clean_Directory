import json
import shutil
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR


class OrganizeFiles:
    """
    This class is used to organize files in a directory by
    moving files into sub-directories based on extention.
    """
    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f'{self.directory} does not exist')
        with open(DATA_DIR / 'extentions.json') as f:
            ext_dirs = json.load(f)
        self.extentions_dest = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extentions_dest[ext] = dir_name

    def __call__(self):
        """Organize files in a directry by moving them
        to sub directories based on extention.
        """
        logger.info(f'Organizing files in {self.directory}...')
        file_extentions = []
        for file_path in self.directory.iterdir():
            # ignore directories
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # move files
            file_extentions.append(file_path.suffix)
            if file_path.suffix not in self.extentions_dest:
                DEST_DIR = self.directory / 'other'
            else:
                DEST_DIR = self.directory / self.extentions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'moving {file_path} to {DEST_DIR}...')
            shutil.move(str(file_path), str(DEST_DIR))


if __name__ == '__main__':
    org_files = OrganizeFiles('/mnt/c/Users/VAIO/Desktop/Python Learning/Hejazi/1-Python/0-My_Python_Practice/4-Project Clean Directory/Clean_Directory/test/kk')
    org_files()
    print('***************Done***************')
