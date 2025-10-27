from colorama import init, Fore, Back, Style

init(autoreset=True)

FORES = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
}

BACKS = {
    "black": Back.BLACK,
    "red": Back.RED,
    "green": Back.GREEN,
    "yellow": Back.YELLOW,
    "blue": Back.BLUE,
    "magenta": Back.MAGENTA,
    "cyan": Back.CYAN,
    "white": Back.WHITE,
}

STYLES = {
    "dim": Style.DIM,
    "normal": Style.NORMAL,
    "bright": Style.BRIGHT,
}


def format_color(text: str, fg: str = None, bg: str = None, style: str = None) -> str:
    """
    Возвращает строку, добавляя в нее ANSI-коды для цвета и стиля.
    """
    color_prefix = ""

    if fg and fg.lower() in FORES:
        color_prefix += FORES[fg.lower()]

    if bg and bg.lower() in BACKS:
        color_prefix += BACKS[bg.lower()]

    if style and style.lower() in STYLES:
        color_prefix += STYLES[style.lower()]

    if not color_prefix:
        return text

    # <КОД_ЦВЕТА> + <ТЕКСТ> + <КОД_СБРОСА>
    return f"{color_prefix}{text}{Style.RESET_ALL}"


def cprint(*args, fg=None, bg=None, style=None, **kwargs):
    """
    Кастомная функция print для вывода цветного текста в консоль.
    """
    color_prefix = ""

    if fg and fg.lower() in FORES:
        color_prefix += FORES[fg.lower()]

    if bg and bg.lower() in BACKS:
        color_prefix += BACKS[bg.lower()]

    if style and style.lower() in STYLES:
        color_prefix += STYLES[style.lower()]

    if not args:
        print(**kwargs)
        return

    new_args = list(args)

    new_args[0] = f"{color_prefix}{str(new_args[0])}"

    # стандартный print с измененными аргументами
    print(*new_args, **kwargs)
