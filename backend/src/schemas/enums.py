"""Enumeration types for the application."""

from enum import Enum


class BottleStatus(str, Enum):
    """Status of a bottle in the collection."""

    SEALED = "sealed"
    OPENED = "opened"
    FINISHED = "finished"
