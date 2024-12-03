"""Common helper methods."""
import logging

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


def setup_logging(name: str) -> logging.Logger:
    """Set up logging to GitHub Actions.logger."""
    root_logger = logging.getLogger(name.rpartition(".")[0])

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
