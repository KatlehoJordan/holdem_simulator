from pathlib import Path

from src.config import logger


def make_dir_if_not_exist(path_to_dir: Path) -> None:
    if not path_to_dir.exists():
        logger.info("%s directory does not exist. Making it now.", path_to_dir)
        path_to_dir.mkdir(parents=True)
