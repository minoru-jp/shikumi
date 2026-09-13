"""Errors raised by Shikumi core semantics."""


class ShikumiError(Exception):
    """Base class for Shikumi errors."""


class UnsupportedFocusError(ShikumiError, TypeError):
    """Raised when a structure cannot interpret a focus."""


class UnknownViewSubjectError(ShikumiError, LookupError):
    """Raised when a subject is not present in a semantic view."""
