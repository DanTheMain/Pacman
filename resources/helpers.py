import tkinter


def get_screen_resolution(scale_factor: float) -> tuple[int, int]:
    """
    note: works for 1/main screen only
    :param scale_factor: the factor of scaling the game window to the current display resolution
    :return: width and height display resolution values
    """
    scale_factor = 0.5 if scale_factor > 1 else scale_factor
    root = tkinter.Tk()
    root.withdraw()
    return int(root.winfo_screenwidth() * scale_factor), int(root.winfo_screenheight() * scale_factor)


