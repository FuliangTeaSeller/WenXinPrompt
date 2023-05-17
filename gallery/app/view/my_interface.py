# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup,QLabel

from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.trie import Trie
class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('Search icons'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)

class myInterface(GalleryInterface):
    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.my,
            subtitle='114514',
            parent=parent
        )
        self.trie = Trie()
        self.iconLibraryLabel = QLabel(self.tr('Prompt库'), self)
        self.searchLineEdit = LineEdit(self)