"""Small identity-based weak registries for runtime semantic facts.

The registry deliberately avoids ``WeakKeyDictionary``. Shikumi's runtime
model is identity-based, while ``WeakKeyDictionary`` follows the key's normal
``__hash__`` / ``__eq__`` semantics. Values stored here must not retain the
subject itself; public records that contain the subject are reconstructed on
read.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from collections.abc import Callable
from typing import Generic, TypeVar
from weakref import ReferenceType, ref

_RecordT = TypeVar("_RecordT")


@dataclass(slots=True)
class _Entry(Generic[_RecordT]):
    subject_ref: ReferenceType[object]
    records: list[_RecordT]


class WeakIdentityRegistry(Generic[_RecordT]):
    """Map weak-referenceable objects to ordered records by object identity."""

    __slots__ = ("_entries", "_lock", "_subject_error")

    def __init__(self, *, subject_error: str) -> None:
        self._entries: dict[int, _Entry[_RecordT]] = {}
        self._lock = RLock()
        self._subject_error = subject_error

    def append(self, subject: object, record: _RecordT) -> None:
        identity = id(subject)
        with self._lock:
            entry = self._entries.get(identity)
            if entry is not None and entry.subject_ref() is subject:
                entry.records.append(record)
                return

            try:
                subject_ref = ref(subject, self._cleanup_callback(identity))
            except TypeError as exc:
                raise TypeError(self._subject_error) from exc

            self._entries[identity] = _Entry(
                subject_ref=subject_ref,
                records=[record],
            )

    def get(self, subject: object) -> tuple[_RecordT, ...]:
        identity = id(subject)
        with self._lock:
            entry = self._entries.get(identity)
            if entry is None or entry.subject_ref() is not subject:
                return ()
            return tuple(entry.records)

    def clear(self, subject: object) -> None:
        identity = id(subject)
        with self._lock:
            entry = self._entries.get(identity)
            if entry is not None and entry.subject_ref() is subject:
                del self._entries[identity]

    def _cleanup_callback(
        self, identity: int
    ) -> Callable[[ReferenceType[object]], None]:
        def cleanup(subject_ref: ReferenceType[object]) -> None:
            with self._lock:
                entry = self._entries.get(identity)
                # ``id`` values can be reused. Only remove the entry whose
                # weakref actually triggered this callback.
                if entry is not None and entry.subject_ref is subject_ref:
                    del self._entries[identity]

        return cleanup
