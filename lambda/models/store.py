from enum import Enum, auto

class Store(str, Enum):
    """Enum for supported stores."""
    AMAZON = "AMAZON"
    NEWEGG = "NEWEGG"
