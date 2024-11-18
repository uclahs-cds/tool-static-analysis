#!/usr/bin/env python3
"""Script to copy fallback linter configuration files into repositories."""

import argparse
import logging
import shutil

from pathlib import Path

NOTICE = 25


class GHAFilter(logging.Filter):
    """A logging filter that plays nice with GitHub Actions output."""

    # pylint: disable=too-few-public-methods

    prefixes = {
        logging.DEBUG: "::debug::",
        logging.INFO: "",
        NOTICE: "::notice::",
        logging.WARNING: "::warning::",
        logging.ERROR: "::error::",
        logging.CRITICAL: "::error::",
    }

    def filter(self, record):
        record.ghaprefix = self.prefixes[record.levelno]
        return True


def setup_logging() -> logging.Logger:
    """Set up logging to GitHub Actions.logger."""
    root_logger = logging.getLogger(__name__.rpartition(".")[0])

    # Does this need to be re-entrant like this?
    if logging.getLevelName("NOTICE") != NOTICE:
        logging.addLevelName(NOTICE, "NOTICE")

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(ghaprefix)s%(message)s"))
        handler.addFilter(GHAFilter())

        # Set these handlers on the root logger of this module
        root_logger.addHandler(handler)
        root_logger.setLevel(logging.DEBUG)

    return root_logger


def copy_configs(config_path: Path, workspace: Path):
    """Copy, without overwriting, all config files into the repository."""
    logger = setup_logging()
    for configfile in config_path.iterdir():
        dest_file = workspace / configfile.name

        if not dest_file.exists() and configfile.is_file():
            shutil.copyfile(configfile, dest_file)
            logger.info("Copying fallback %s", configfile.name)
        else:
            logger.info("Repository already has %s", configfile.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=Path)
    parser.add_argument("workspace", type=Path)

    args = parser.parse_args()

    copy_configs(args.config_path, args.workspace)
