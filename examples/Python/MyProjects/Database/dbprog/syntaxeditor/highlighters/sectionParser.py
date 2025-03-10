""" sectionParser.py: utility class to parse a section of the syntax.ini """
import os
import pathlib
from configparser import ConfigParser
import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


def usingDarkTheme() -> bool:
    """
    utility function to determine if current OS theme is light or dark
    @see: https://stackoverflow.com/questions/65294987/detect-os-dark-mode-in-python
    """
    color = QApplication.instance().palette().base().color()
    theme: str = ""
    r, g, b, a = color.getRgb()
    hsp = math.sqrt((0.241 * r * r) + (0.691 * g * g) + (0.068 * b * b))
    # theme = "light" if hsp > 127.5 else "dark"
    # return theme == "dark"
    return hsp <= 127.5


def parseSection(section: str, subkey: str) -> (str, QTextCharFormat):
    """parses entries under 'subkey' of a 'section' of the syntax.cfg file,
        which follows the INI file format
    @params:
        section: the section to look under
        subkey: the subkey whose values are to be parsed
    @returns: a tuple of 2 values
        tuple(0) - subkey values split and combined into a raw string
            like this r'\bval1\b|\bval2\b|...|\bvalN\b'
            NOTE: this could be a NULL if subkey is not found
        tuple(1) - a QTextFormatObject
    """
    config_file_path = pathlib.Path(__file__).parent / "syntax.cfg"
    assert os.path.exists(
        str(config_file_path)
    ), f"FATAL ERROR: unable to locate syntax configuration file (syntax.ini)"

    parser = ConfigParser()
    parser.read(str(config_file_path))
    assert parser.has_section(
        section
    ), f"FATAL ERROR: expecting section [SQL] in syntax config file (syntax.ini)"

    sep_pat = r"\b"
    subkey_pat = ""
    subkey_str = parser.get(section, subkey, fallback=None)
    if subkey_str is not None:
        subkey_items = subkey_str.split(",")
        for key in subkey_items:
            key = f"{sep_pat}{key.strip()}{sep_pat}|"
            subkey_pat += key
        if subkey_pat.endswith("|"):
            subkey_pat = subkey_pat[: len(subkey_pat) - 1]

    formatter = None
    if usingDarkTheme():
        subkey_color_style = parser.get(
            section, f"{subkey}_color_style_dark", fallback=None
        )
    else:
        subkey_color_style = parser.get(section, f"{subkey}_color_style", fallback=None)

    if subkey_color_style is not None:
        subkey_color, subkey_bold, subkey_italic = subkey_color_style.split(",")
        font_bold = True if subkey_bold.strip() == "1" else False
        font_italic = True if subkey_italic.strip() == "1" else False
        formatter = QTextCharFormat()
        formatter.setForeground(QBrush(QColor(subkey_color)))
        if font_bold:
            formatter.setFontWeight(QFont.Weight.Bold)
        if font_italic:
            formatter.setFontItalic(True)

    return subkey_pat, formatter
