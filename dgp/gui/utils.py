# coding: utf-8

import logging
from pathlib import Path
from typing import Union, Callable

LOG_FORMAT = logging.Formatter(
    fmt="%(asctime)s:%(levelname)s - %(module)s:%(funcName)s :: %(message)s",
        datefmt="%H:%M:%S")
LOG_COLOR_MAP = {'debug': 'blue', 'info': 'yellow', 'warning': 'brown',
                 'error': 'red', 'critical': 'orange'}
LOG_LEVEL_MAP = {'debug': logging.DEBUG, 'info': logging.INFO,
                 'warning': logging.WARNING, 'error': logging.ERROR,
                 'critical': logging.CRITICAL}


class ConsoleHandler(logging.Handler):
    """
    Custom Logging Handler allowing the specification of a custom logging
    destination or method via the passing of an external function.

    e.g. Passing of a PyQt slot that outputs any input string to a QtTextArea

    If the destination Callable does not accept two parameters, the emit()
    method will attempt to emit the message as a single parameter to the
    destination.

    Parameters
    ----------
    destination: Callable[[str, str], None]
        Callable with signature str -> str -> None.
        Callable should accept a message (str) and level name (str)
    """
    def __init__(self, destination: Callable[[str, str], None]):
        super().__init__()
        self._dest = destination

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit the log record to the destination, first running it through any
        specified formatter.

        Parameters
        ----------
        record: logging.LogRecord
            Log record to emit via the destination specified on instantiation.
        """
        entry = self.format(record)
        try:
            self._dest(entry, record.levelname.lower())
        except TypeError:
            self._dest(entry)


def get_project_file(path: Path) -> Union[Path, None]:
    """
    Attempt to retrieve a project file (\*.d2p) from the given dir path,
    otherwise signal failure by returning False.

    Parameters
    ----------
    path: Path
        Directory path to search for DGP project file.
        If supplied path is not a directory, attempt to resolve the parent
        and search from there.

    Returns
    -------
    Path:
        First resolved path to DGP project file (\*.d2p)
    """
    if not path.is_dir():
        path = path.parent
    for child in sorted(path.glob('*.d2p')):
        return child.resolve()
    return None
