from enum import Enum, auto


class Get_key_modes(Enum):
    NO_IGNORE = auto()
    IGNORE_HORIZONTAL = auto()
    IGNORE_VERTICAL = auto()
    IGNORE_ESCAPE = auto()
    IGNORE_ENTER = auto()


class Keys(Enum):
    ESCAPE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()


def get_key(mode:Get_key_modes=Get_key_modes.NO_IGNORE, key_map:tuple[list[list[list[bytes]]], list[bytes]]=None):
    """
    Function for detecting a keypress (mainly arrow keys)\n
    Returns a value from the `Key` enum depending on the key type.\n
    Throws an error if msvcrt/getch was not found. (this module is windows only)\n
    Depending on the mode, it ignores some keys:\n
    \tNO_IGNORE: don't ignore any key
    \tIGNORE_HORIZONTAL: ignore left/right
    \tIGNORE_VERTICAL: ignore up/down
    \tIGNORE_ESCAPE: ignore escape
    \tIGNORE_ENTER: ignore enter\n
    You can set custom keys keybinds by providing a key_map:\n
    [[a list for each value in the `Key` enum, with each list having 2 lists of keys (the 1. list containing the keys that aren't arrow keys, the 2. containing the ones that are)], [double (arrow) key 1. halfs]]\n
    Examles:\n
    \tdefault: ([[[b"\\x1b"]], [[], [b"H"]], [[], [b"P"]], [[], [b"K"]], [[], [b"M"]], [[b"\\r"]]], [b"\\xe0", b"\\x00"])
    \tarrow/WASD: ([[[b"\\x1b", b"e"]], [[b"w"], [b"H"]], [[b"s"], [b"P"]], [[b"a"], [b"K"]], [[b"d"], [b"M"]], [[b"\\r", b" "]]], [b"\\xe0", b"\\x00"])
    \tonly W, A, and D without setting the mode: ([[], [[b"w"]], [], [[b"a"]], [[b"d"]], []])
    \tunintended/compressed: ([[b"\\x1b"], [[], b"H"], [[], b"P"], [[], b"K"], [[], b"M"], [b"\\r"]], b"\\xe0\\x00")
    """
    try:
        from msvcrt import getch
    except ModuleNotFoundError:
        raise ModuleNotFoundError("msvcrt module not found!\nThis module is windows only!")
    
    ignore_list = [Get_key_modes.IGNORE_ESCAPE, Get_key_modes.IGNORE_VERTICAL, Get_key_modes.IGNORE_VERTICAL,
                   Get_key_modes.IGNORE_HORIZONTAL, Get_key_modes.IGNORE_HORIZONTAL, Get_key_modes.IGNORE_ENTER]
    response_list = [Keys.ESCAPE, Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT, Keys.ENTER]
    
    arrow = False
    if key_map is None:
        key_map = ([[[b"\x1b"]], [[], [b"H"]], [[], [b"P"]], [[], [b"K"]], [[], [b"M"]], [[b"\r"]]], [b"\xe0", b"\x00"])
    while True:
        key = getch()
        # print(key)
        arrow = False
        if len(key_map) != 1 and len(key_map) > 1 and key in key_map[1]:
            arrow = True
            key = getch()
            # print("arrow", key)
        
        for x in range(len(response_list)):
            if ((not arrow and len(key_map[0][x]) > 0 and key in key_map[0][x][0]) or
                (arrow and len(key_map[0][x]) > 1 and key in key_map[0][x][1])) and mode != ignore_list[x]:
                return response_list[x]


def imput(ask="Num: "):
    """Input but only accepts whole numbers."""
    while True:
        try: return int(input(ask))
        except ValueError: print("Not a number!")