"""
This module has functions for a displaying basic UI elements using the terminal, with the `screen_display` module.
"""
__version__ = "0.1"


if __name__ == "__main__":
    from cursor import Cursor_icon
    from ui_list import UI_list, UI_list_s, UI_list_button
    from options_ui import Base_UI, Choice, Slider, Toggle, Button, UINoSelectablesError, options_ui
    from utils import get_key, Get_key_modes, Keys, imput
else:
    from terminal_ui.cursor import Cursor_icon
    from terminal_ui.ui_list import UI_list, UI_list_s, UI_list_button
    from terminal_ui.options_ui import Base_UI, Choice, Slider, Toggle, Button, UINoSelectablesError, options_ui
    from terminal_ui.utils import get_key, Get_key_modes, Keys, imput


# def over(a=5, b=1, c="def c", d="def d", e="def e", f="def f", g="def g"):
#     input(f"{a}, {b}, {c}, {d}, {e}, {f}")

# def mod(li:list[list]):
#     print(li)
#     if len(li[0]) == len(li[1]):
#         li[1].pop(-1)
#     li[0].pop(-1)
#     if len(li[0]) == 0:
#         return -1


# l3_0 = UI_list(["option 1", "option 2", "back"], "l3_0", can_esc=True, action_list=[[over, 15, "gfg", UI_list, {"d":"d"}, {"f":59}], [input, "nummm: "], None])
# l2_0 = UI_list(["option 1", "option 2", "l3_0", "back"], "l2_0", can_esc=True, action_list=[imput, imput, l3_0, None])
# l2_1 = UI_list(["option 1", "option 2", "back"], "l2_1", can_esc=True, action_list=[imput, imput, 0])
# l2_2 = UI_list(["option 1", "option 2", "back"], "l2_2", can_esc=True, action_list=[imput, imput, 0])
# l1_0 = UI_list(["option 1", "option 2", "l2_2", "back"], "l1_0", can_esc=True, action_list=[imput, imput, l2_2, 0])
# l1_1 = UI_list(["option 1", "option 2", "l2_1", "l2_0", "back"], "l1_1", can_esc=True, action_list=[imput, imput, l2_1, l2_0, None])
# l0 = UI_list(["function", "l1_0", "\nl1_1", "\nExit", "function", "l1_0\n", "l1_1", "Exit", "function", "l1_0", "l1_1", "Exit"], "Main menu", multiline=False, action_list=[mod, l1_0, l1_1, None], modify_list=True)

# l0.display()




# print(UI_list(["\n1", "\n2", "\n3", None, None, None, "Back", None, None, "\n\n\nlol\n"], "Are you old?", Cursor_icon("-->", "<--", "  #", "#  "), True).display())

# def lolno():
#     return False

# elements = []
# elements.append(Slider(13, 5, "\nslider test 1\n|", "#", "-", "|\n", True, "$\n", True))
# elements.append(None)
# elements.append("2. test")
# elements.append(Slider(range(2, 20, 2), 15, "slider test 2 |", "#", "-", "| ", True, "l"))
# elements.append(Choice(["h", "j\nt", "l", 1], 2, "choice test ", " lol ", True, "$", True))
# elements.append(Toggle(1, "toggle test ", post_value=" $"))
# elements.append(UI_list_s(["one"]))
# elements.append(UI_list_s(["two"]))
# elements.append(None)
# elements.append(UI_list_button("three", lolno))
# elements.append(Button("yes", lolno))
# elements.append(Button("hmmm", UI_list_s(["hm", "l"], "kk", can_esc=True)))

# print(options_ui(elements, "test", Cursor_icon(">", "<")))

# for element in elements:
#     if isinstance(Base_UI, element):
#         print(element.pre_text + str(element.value))
