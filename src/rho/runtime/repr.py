"""OCaml-style value representation: tag constants and layout.

Every value is one word (e.g. 64-bit):
- Immediate: low bit = 1; remaining bits encode small integers (n << 1 | 1).
- Pointer: low bit = 0; points to a heap block.

Heap block: header word (tag byte, size, GC color) then payload.
Tags >= NO_SCAN_TAG mean payload is opaque (e.g. float, bytes); GC does not scan.
"""

# Tag byte ranges (same idea as OCaml)
TAG_TUPLE = 0
TAG_ARRAY = 1
TAG_CLOSURE = 2
TAG_FLOAT = 251  # opaque
TAG_STRING = 252
NO_SCAN_TAG = 251


def is_immediate(word: int) -> bool:
    return (word & 1) != 0


def untag_int(word: int) -> int:
    return word >> 1


def tag_int(n: int) -> int:
    return (n << 1) | 1
