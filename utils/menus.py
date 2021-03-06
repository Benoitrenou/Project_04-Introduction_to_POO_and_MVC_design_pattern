class Menu:
    """Object Menu builder"""

    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add(self, key, option, handler):
        """Add a MenuEntry to the Menu."""
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1

        self._entries[str(key)] = MenuEntry(option, handler)

    def items(self):
        """Apply items function to Menu entries."""
        return self._entries.items()

    def __contains__(self, choice):
        return str(choice) in self._entries

    def __getitem__(self, choice):
        return self._entries[choice]


class MenuEntry:
    """Object Menu entry builder"""

    def __init__(self, option, handler):
        self.option = option
        self.handler = handler

    def __repr__(self):
        return f"MenuEntry({self.option}, {self.handler})"

    def __str__(self):
        return str(self.option)
