
class Cursor_icon():
    """Cursor icon object for UI objects."""

    def __init__(self, selected_icon:str = ">", selected_icon_right:str = "", not_selected_icon:str = " ", not_selected_icon_right:str = ""):
        self.s_icon = str(selected_icon)
        self.s_icon_r = str(selected_icon_right)
        self.icon = str(not_selected_icon)
        self.icon_r = str(not_selected_icon_right)