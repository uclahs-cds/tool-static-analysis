#!/usr/bin/env python3
"""Script to copy fallback linter configuration files into repositories."""

import argparse
import logging
import shutil

from pathlib import Path

from ruamel.yaml import YAML

from analysishelper import setup_logging


def copy_configs(config_path: Path, workspace: Path):
    """Copy, without overwriting, all config files into the repository."""
    logger = setup_logging(__name__)
    for configfile in config_path.iterdir():
        if not configfile.is_file():
            continue

        dest_file = workspace / configfile.name

        if not dest_file.exists():
            shutil.copyfile(configfile, dest_file)
            logger.info("Copying fallback %s", configfile.name)
        elif configfile.name == ".mega-linter.yml":
            logger.info("Merging %s with existing config", configfile.name)
            merge_megalinter_config(configfile, dest_file)
        else:
            logger.info("Repository already has %s", configfile.name)


def merge_megalinter_config(fallback_config: Path, existing_config: Path):
    """"
    Merge the repository's megalinter configuration with the bundled configuration.
    """
    logger = logging.getLogger(__name__)

    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    fallback_data = yaml.load(fallback_config)
    existing_data = yaml.load(existing_config)

    # We depend on the exact values of these configuration arguments
    overwrite_keys = {
        "BASH_SHELLCHECK_ARGUMENTS",
        "JSON_REPORTER",
        "JSON_REPORTER_OUTPUT_DETAIL",
    }

    # We can only support certain values of these keys
    intersect_keys = {"ENABLE"}

    for key, value in fallback_data.items():
        if key in existing_data:
            if key in overwrite_keys:
                # Stomp over these values
                if value != existing_data[key]:
                    logger.warning(
                        "Overriding MegaLinter config value %s from %s to %s",
                        key,
                        existing_data[key],
                        value
                    )
                    existing_data[key] = value

            elif key in intersect_keys:
                # Filter these values
                original_value = set(existing_data[key])
                updated_value = original_value & set(value)

                if (lost_keys := original_value - updated_value):
                    logger.warning(
                        "Removing values from MegaLinter config %s: %s (leaving %s)",
                        key,
                        sorted(lost_keys),
                        sorted(updated_value),
                    )
                    existing_data[key] = sorted(updated_value)

            else:
                # Respect the original
                logger.info(
                    "Deferring to local MegaLinter config value %s: %s",
                    key,
                    existing_data[key]
                )
        else:
            # Inject the new value
            logger.info(
                "Adding MegaLinter config value %s: %s",
                key,
                value
            )
            existing_data[key] = value

    yaml.dump(existing_data, existing_config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_path", type=Path)
    parser.add_argument("workspace", type=Path)

    args = parser.parse_args()

    copy_configs(args.config_path, args.workspace)
