# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup,QLabel, QFrame, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme, PushButton, InfoBar, InfoBarIcon, InfoBarPosition,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit)
from qfluentwidgets import LineEdit
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.trie import Trie
import json
import os
class LineEdit1(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('Search icons'))
        self.setFixedWidth(305)
        self.textChanged.connect(self.search)
class LineEdit2(LineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(305)
        self.setFixedHeight(100)
class editPromptInterface(GalleryInterface):
    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.my,
            subtitle='',
            parent=parent
        )
        self.trie = Trie()
        self.view = QWidget(self)
        self.button = PushButton(self.tr('create'))
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.create_json)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
    def __initWidget(self):
        self.view.setObjectName('view')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.addPropmtCard("Title", 100, 50)
        self.addPropmtCard("Explanation", 200, 100)
        self.addPropmtCard("Exactinfo", 200, 200)
        self.vBoxLayout.addWidget(self.button)

    def addPropmtCard(self, title, width, height):
        card = CreatepromptCard(title, width, height)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
        return card

    def create_json(self):
        data = {"prompts": []}
        card_dict = {}  # Create a single dictionary for the prompt
        for index in range(self.vBoxLayout.count() - 1):  # Exclude the last widget which is the button
            card = self.vBoxLayout.itemAt(index).widget()
            if isinstance(card, CreatepromptCard):
                key = card.label.text()
                value = card.lineedit.text()
                card_dict[key] = value  # Add key-value pair to the same dictionary
        data["prompts"].append(card_dict)  # Add the prompt dictionary to "prompts" after the loop ends
        # Ensure the directory exists
        directory = "./app/resource/prompts"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Get the "Title" field from the data
        filename = card_dict.get("Title", "default")  # Use a default filename if "Title" does not exist
        # Save data as json
        with open(os.path.join(directory, filename + ".json"), "w") as file:
            json.dump(data, file, ensure_ascii=False)
        InfoBar.success("成功", "文件已成功创建！", parent=self)
#创建一个card，包括一个label和一个lineedit
class CreatepromptCard(QFrame):
    def __init__(self, title='Title', width=100, height=50):
        super().__init__()
        self.label = QLabel(title, self)
        self.label.setFixedWidth(80)
        self.lineedit = LineEdit2()
        self.lineedit.setText('n m s l')
        self.lineedit.setFixedWidth(width)
        self.lineedit.setFixedHeight(height)
        self.lineedit.setClearButtonEnabled(True)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label)
        self.hBoxLayout.addWidget(self.lineedit)
        self.hBoxLayout.setSpacing(10)
        self.hBoxLayout.setContentsMargins(0,0,0,0)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)



