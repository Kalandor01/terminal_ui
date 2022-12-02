from typing import Callable

from terminal_ui.cursor import Cursor_icon
from terminal_ui.ui_list import UI_list
from terminal_ui.utils import get_key, Get_key_modes, Keys
# from cursor import Cursor_icon
# from ui_list import UI_list
# from utils import get_key, Get_key_modes, Keys


class UINoSelectablesError(Exception):
    """Exeption raised when there are no values in the selectables list in the `options_ui` function."""
    pass

class Base_UI:
    """
    Base class for all `options_ui` classes.\n
    Structure: [pre_text][#####][pre_value][value][post_value]
    """
    def __init__(self, value=0, pre_text="", pre_value="", display_value=False, post_value="", multiline=False):
        self.value:int = int(value)
        self.pre_text:str = str(pre_text)
        self.pre_value:str = str(pre_value)
        self.display_value:bool = bool(display_value)
        self.post_value:str = str(post_value)
        self.multiline:bool = bool(multiline)
    
    
    def _clamp_value(self, value:int, v_min:int, v_max:int):
        value = int(value)
        if value > v_max:
            value = v_max
        elif value < v_min:
            value = v_min
        return value
    
    
    def make_text(self, icon:str, icon_r:str):
        """
        Returns the text representation of the UI element.
        """
        txt = ""
        # current icon group
        icons = f"{icon_r}\n{icon}"
        # icon
        txt += icon
        # pre text
        if self.multiline:
            txt += self.pre_text.replace("\n", icons)
        else:
            txt += self.pre_text
        # special
        txt += self._make_special(icons)
        # pre value
        if self.multiline:
            txt += self.pre_value.replace("\n", icons)
        else:
            txt += self.pre_value
        # value
        if self.display_value:
            txt += self._make_value()
        # post value
        if self.multiline:
            txt += self.post_value.replace("\n", icons)
        else:
            txt += self.post_value
        # icon right
        txt += icon_r + "\n"
        return txt
    
    
    def _make_special(self, icons_str:str) -> str:
        """
        Returns the string representation of the cpecial varable.
        """
        return ""
    
    
    def _make_value(self):
        """
        Returns the string representation of the value.
        """
        return str(self.value)
    
    
    def _handle_action(self, key:Keys, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
        """
        Handles what to return for the input key.\n
        Returns False if the screen should not update.
        """
        return True


class Slider(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a slider, with the section specifying it's characteristics.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol and symbol_empty][pre_value][value][post_value]
    """
    def __init__(self, value_range:int|range, value=0, pre_text="", symbol="#", symbol_empty="-", pre_value="", display_value=False, post_value="", multiline=False):
        if type(value_range) is range:
            self.value_range = value_range
        elif type(value_range) is int:
            self.value_range = range(value_range)
        else:
            raise TypeError
        value = super()._clamp_value(value, min(self.value_range.start, self.value_range.stop), max(self.value_range.start, self.value_range.stop))
        super().__init__(value, pre_text, pre_value, display_value, post_value, multiline)
        self.symbol = str(symbol)
        self.symbol_empty = str(symbol_empty)
    
    
    def _make_special(self, icons_str:str):
        txt = ""
        for x in self.value_range:
            txt += (self.symbol_empty if x >= self.value else self.symbol)
        return txt
    
    
    def _handle_action(self, key:Keys, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
        if key == Keys.RIGHT:
            if self.value + self.value_range.step <= self.value_range.stop:
                self.value += self.value_range.step
            else:
                return False
        else:
            if self.value - self.value_range.step >= self.value_range.start:
                self.value -= self.value_range.step
            else:
                return False
        return True


class Choice(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a multiple choice seletion, with the choice_list list specifying the choice names.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][choice name][pre_value][value][post_value]
    """
    def __init__(self, choice_list:list|range, value=0, pre_text="", pre_value="", display_value=False, post_value="", multiline=False):
        value = super()._clamp_value(value, 0, len(choice_list) - 1)
        super().__init__(value, pre_text, pre_value, display_value, post_value, multiline)
        choice_list = [str(choice) for choice in choice_list]
        self.choice_list = list(choice_list)


    def _make_special(self, icons_str:str):
        if self.multiline:
            return self.choice_list[self.value].replace("\n", icons_str)
        else:
            return self.choice_list[self.value]
    
    
    def _make_value(self):
        return f"{self.value + 1}/{len(self.choice_list)}"
    
    
    def _handle_action(self, key:Keys, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
        if key == Keys.RIGHT:
            self.value += 1
        elif key == Keys.LEFT:
            self.value -= 1
        self.value = self.value % len(self.choice_list)
        return True


class Toggle(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it draws a field that is toggleable with the enter key.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [pre_text][symbol or symbol_off][post_value]
    """
    def __init__(self, value=0, pre_text="", symbol="on", symbol_off="off", post_value="", multiline=False):
        value = super()._clamp_value(value, 0, 1)
        super().__init__(value, pre_text, "", False, post_value, multiline)
        self.symbol = str(symbol)
        self.symbol_off = str(symbol_off)
        
    
    def _make_special(self, icons_str:str):
        return (self.symbol_off if self.value == 0 else self.symbol)
    
    
    def _handle_action(self, key: Keys, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
        if key == Keys.ENTER:
            self.value = int(not bool(self.value))
        return True


class Button(Base_UI):
    """
    Object for the options_ui method\n
    When used as input in the options_ui function, it text that is pressable with the enter key.\n
    If `action` is a function (or a list with a function as the 1. element, and arguments as the 2-n. element, including 1 or more dictionaries as **kwargs), it will run that function, if the button is clicked.\n
    - If the function returns False the screen will not rerender.\n
    - If it is a `UI_list` object, the object's `display` function will be automaticly called, allowing for nested menus.\n
    - If `modify` is `True`, the function (if it's not a `UI_list` object) will get a the `Button` object as it's first argument (and can modify it) when the function is called.\n
    Multiline makes the "cursor" draw at every line if the text is multiline.\n
    Structure: [text]
    """
    def __init__(self, text="", action:Callable=None, multiline=False, modify=False):
        super().__init__(-1, text, "", False, "", multiline)
        self.action = action
        self.modify = bool(modify)
    
    
    def _handle_action(self, key: Keys, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
        if key == Keys.ENTER:
            # list
            if type(self.action) is list and len(self.action) >= 2:
                lis = []
                di = dict()
                for elem in self.action:
                    if type(elem) is dict:
                        di.update(elem)
                    else:
                        lis.append(elem)
                if self.modify:
                    func_return = lis[0](self, *lis[1:], **di)
                else:
                    func_return = lis[0](*lis[1:], **di)
                if func_return is None:
                    return True
                else:
                    return bool(func_return)
            # normal function
            elif callable(self.action):
                if self.modify:
                    func_return = self.action(self)
                else:
                    func_return = self.action()
                if func_return is None:
                        return True
                else:
                    return bool(func_return)
            # ui
            else:
                # display function or lazy back button
                try:
                    self.action.display(key_mapping=key_mapping)
                except AttributeError:
                    # print("Option is not a UI_list object!")
                    pass
                return True
        else:
            return True


def options_ui(elements:list[Base_UI|UI_list], title:str=None, cursor_icon:Cursor_icon=None, key_mapping:tuple[list[list[list[bytes]]], list[bytes]]=None):
    """
    Prints the title and then a list of elements that the user can cycle between with the up and down arrows, and adjust with either the left and right arrow keys or the enter key depending on the input object type, and exit with Escape.\n
    Accepts mainly a list of objects (Slider, Choice, Toggle (and UI_list)).\n
    if an element in the list is not one of these objects, the value will be printed, (or if it's None, the line will be blank) and cannot be selected.
    """
    if cursor_icon is None:
        cursor_icon = Cursor_icon()
    # is enter needed?
    no_enter = True
    for element in elements:
        if isinstance(element, (Toggle, UI_list)):
            no_enter = False
            break
    # put selected on selectable
    selected = 0
    while not isinstance(elements[selected], (Base_UI, UI_list)):
        selected += 1
        if selected >= len(elements):
            raise UINoSelectablesError("No selectable element in the elements list.")
    # render/getkey loop
    key = None
    while key != Keys.ESCAPE:
        # render
        # clear screen
        txt = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        if title is not None:
            txt += title + "\n\n"
        for x in range(len(elements)):
            element = elements[x]
            # UI elements
            if isinstance(element, Base_UI):
                txt += element.make_text(
                    (cursor_icon.s_icon if selected == x else cursor_icon.icon),
                    (cursor_icon.s_icon_r if selected == x else cursor_icon.icon_r))
            # UI_list
            elif isinstance(element, UI_list):
                # txt += element.__make_text(selected)
                # render
                if element.answer_list[0] is not None:
                    if selected == x:
                        curr_icon = element.cursor_icon.s_icon
                        curr_icon_r = element.cursor_icon.s_icon_r
                    else:
                        curr_icon = element.cursor_icon.icon
                        curr_icon_r = element.cursor_icon.icon_r
                    txt += curr_icon + (element.answer_list[0].replace("\n", f"{curr_icon_r}\n{curr_icon}") if element.multiline else element.answer_list[0]) + f"{curr_icon_r}\n"
                else:
                    txt += "\n"
            elif element is None:
                txt += "\n"
            else:
                txt += str(element) + "\n"
        print(txt)
        # move selection/change value
        actual_move = False
        while not actual_move:
            # to prevent useless screen re-render at slider
            actual_move = True
            # get key
            key = Keys.ENTER
            if isinstance(elements[selected], (Toggle, Button, UI_list)):
                key = get_key(Get_key_modes.IGNORE_HORIZONTAL, key_mapping)
            else:
                while key == Keys.ENTER:
                    key = get_key(Get_key_modes.NO_IGNORE, key_mapping)
                    if key == Keys.ENTER and no_enter:
                        key = Keys.ESCAPE
            # move selection
            if key == Keys.UP or key == Keys.DOWN:
                while True:
                    if key == Keys.DOWN:
                        selected += 1
                        if selected > len(elements) - 1:
                            selected = 0
                    else:
                        selected -= 1
                        if selected < 0:
                            selected = len(elements) - 1
                    if isinstance(elements[selected], (Base_UI, UI_list)):
                        break
            # change value Base_UI
            elif isinstance(elements[selected], Base_UI) and (key in [Keys.LEFT, Keys.RIGHT, Keys.ENTER]):
                actual_move = bool(elements[selected]._handle_action(key, key_mapping))
            # change value UI_list
            elif isinstance(elements[selected], UI_list) and key == Keys.ENTER:
                action = elements[selected]._handle_action(0, key_mapping)
                if action is not None:
                    return action