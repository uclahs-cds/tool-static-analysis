#!/usr/bin/env python3
"Generate an action.yml file from the template."
import os
import re
from pathlib import Path

# Bail out if there are any illegal characters in the tag
tag = os.environ.get("DOCKER_IMAGE_TAG")
if re.search(r"[^a-zA-Z0-9_.\-]", tag):
    raise ValueError(f"Problem with the tag `{tag}`!")

template = Path(os.environ.get("GITHUB_ACTION_PATH"), "template", "action.yml")
output_file = Path(os.environ.get("GITHUB_WORKSPACE"), ".git", "action.yml")

output_file.write_text(
    template.read_text(encoding="utf-8").replace(
        "DOCKER_IMAGE_TAG", tag
    ),
    encoding="utf-8"
)
