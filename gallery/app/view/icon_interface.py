# coding:utf-8
from typing import List

from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal,QTimer
from PyQt5.QtWidgets import QApplication, QFrame, QVBoxLayout, QLabel, QWidget, QHBoxLayout
from qfluentwidgets import (FluentIcon, IconWidget, FlowLayout, isDarkTheme,PushButton,
                            Theme, applyThemeColor, SmoothScrollArea, SearchLineEdit)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..common.trie import Trie
import json
def splitText(text: str, maxLineLength: int) -> str:
        words = text.split(' ')
        lines = []
        currentLine = []
        currentLength = 0

        for word in words:
            if currentLength + len(word) > maxLineLength and currentLine:
                lines.append(' '.join(currentLine))
                currentLine = []
                currentLength = 0

            currentLine.append(word)
            currentLength += len(word) + 1  # "+ 1" is for the space

        if currentLine:  # Add the last line if it's not empty
            lines.append(' '.join(currentLine))

        return '\n'.join(lines)
class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('Search prompts'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)


class PromptCard(QFrame):
    """ Icon card """

    clicked = pyqtSignal(FluentIcon)

    def __init__(self, icon: FluentIcon, parent=None,prompt=None):
        super().__init__(parent=parent)
        self.icon = icon
        self.isSelected = False

        self.prompt = prompt
        self.iconWidget = IconWidget(icon, self)
        self.mainNameLabel = QLabel(self)
        self.subNameLabel = QLabel(self)
        self.vBoxLayout = QVBoxLayout(self)
        # self.setFixedSize(96, 96)
        self.setFixedSize(192, 96)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(8, 28, 8, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        # self.iconWidget.setFixedSize(28, 28)
        self.iconWidget.setFixedSize(28, 28)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft)
        self.vBoxLayout.addSpacing(14)
        self.vBoxLayout.addWidget(self.mainNameLabel, 0, Qt.AlignHCenter)

        maintext = self.mainNameLabel.fontMetrics().elidedText(prompt["title"], Qt.ElideLeft, 78)
        subtext = self.mainNameLabel.fontMetrics().elidedText(prompt["explanation"], Qt.ElideLeft, 150)#对一个过长的字符串进行裁剪，以便它能在给定的宽度内显示。
        font = QFont()
        font.setFamily('Arial')
        font.setPointSize(14)
        # font.setBold(True)
        self.mainNameLabel.setStyleSheet('color: grey;')
        self.mainNameLabel.setText(maintext)
        self.mainNameLabel.setFont(font)
        # self.subNameLabel.setText(subtext)
        # self.mainNameLabel.setStyleSheet('font-family: Arial; font-weight: bold;')
        

    def mouseReleaseEvent(self, e):
        if self.isSelected:
            return

        self.clicked.emit(self.icon)

    def setSelected(self, isSelected: bool, force=False):
        if isSelected == self.isSelected and not force:
            return

        self.isSelected = isSelected

        if not isSelected:
            # self.iconWidget.setIcon(self.icon)
            self.mainNameLabel.setStyleSheet('color: grey;font-weight: normal;')
        else:
            # icon = self.icon.icon(Theme.LIGHT if isDarkTheme() else Theme.DARK)
            self.mainNameLabel.setStyleSheet('color: rgb(0, 159, 170);font-weight: bold;')
            # self.iconWidget.setIcon(icon)

        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())


class IconInfoPanel(QFrame):
    """ Icon info panel """

    def __init__(self, icon: FluentIcon, prompt,parent=None):
        super().__init__(parent=parent)
        self.prompt=prompt
        self.nameLabel = QLabel(icon.value, self)
        self.iconWidget = IconWidget(icon, self)
        self.iconNameTitleLabel = QLabel(self.tr('详细介绍'), self)
        self.iconNameLabel = QLabel(icon.value, self)
        self.enumNameTitleLabel = QLabel(self.tr('prompt正文'), self)
        self.enumNameLabel = QLabel("abc" + icon.name, self)

        self.copyButton=PushButton(self.tr('复制'))
        self.copyButton.clicked.connect(self.copyTextToClipboard)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(16, 20, 16, 20)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.vBoxLayout.addWidget(self.nameLabel)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(15)
        self.vBoxLayout.addWidget(self.iconNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.iconNameLabel)
        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.enumNameTitleLabel)
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.enumNameLabel)
        self.vBoxLayout.addStretch()
        self.vBoxLayout.addWidget(self.copyButton)
        

        self.iconWidget.setFixedSize(0, 0)
        self.setFixedWidth(216)

        self.nameLabel.setObjectName('nameLabel')
        self.iconNameTitleLabel.setObjectName('subTitleLabel')
        self.enumNameTitleLabel.setObjectName('subTitleLabel')
    

        
    # def setIcon(self, icon: FluentIcon,prompt=None):     
    #     self.iconWidget.setIcon(icon)
    #     self.nameLabel.setText(prompt["title"])
    #     self.iconNameLabel.setText(prompt["explanation"])
    #     self.enumNameLabel.setText(prompt["exactinfo"])
    #     self.prompt=prompt
    
    
    
    def setIcon(self, icon: FluentIcon,prompt=None):     
        self.iconWidget.setIcon(icon)
        self.nameLabel.setText(splitText(prompt["title"], 20))
        self.iconNameLabel.setText(splitText(prompt["explanation"], 30))  # Use splitText function here
        self.enumNameLabel.setText(splitText(prompt["exactinfo"], 30))  # And here
        self.prompt=prompt

    def copyTextToClipboard(self):
        clipboard = QApplication.clipboard()  # 获取剪贴板实例
        clipboard.setText(self.prompt["exactinfo"])  # 将 exactinfo 文本设置到剪贴板中
        
    
class IconCardView(QWidget):
    """ Icon card view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.trie = Trie()
        self.iconLibraryLabel = QLabel(self.tr('在本地prompt库中搜索'), self)
        self.searchLineEdit = LineEdit(self)

        self.view = QFrame(self)
        self.scrollArea = SmoothScrollArea(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.infoPanel = IconInfoPanel(FluentIcon.MENU, self)

        self.vBoxLayout = QVBoxLayout(self)#搜索栏
        self.hBoxLayout = QHBoxLayout(self.view)#右侧面板
        self.flowLayout = FlowLayout(self.scrollWidget, isTight=True)
        self.cvLayout=QHBoxLayout(self)

        self.cards = []     # type:List[PromptCard]
        self.icons = []
        self.myExtraInfos = []
        self.currentIndex = -1

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(0, 5, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self.iconLibraryLabel)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.vBoxLayout.addWidget(self.view)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.addWidget(self.infoPanel, 0, Qt.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)
    
        # self.cvLayout.addWidget(self.copyButton)

        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)
        self.searchLineEdit.clearSignal.connect(self.showAllIcons)
        self.searchLineEdit.searchSignal.connect(self.search)
        
        # 打开并读取JSON文件
        with open('./gallery/app/resource/prompts.json', 'r') as f:
            data = json.load(f)

        # 获取prompts列表
        prompts = data['prompts']
        for prompt in prompts:
            self.addPrompt(prompt)
        self.showAllIcons()
        self.setSelectedIcon(self.icons[0])
        self.searchLineEdit.setText("Prompt Here")
        for card in self.cards:
            card.hide()
            

    def addPrompt(self,prompt):
        """ add icon to view """
        icon=FluentIcon(prompt["icon"])
        card = PromptCard(icon, self,prompt)
        card.clicked.connect(self.setSelectedIcon)

        self.cards.append(card)
        self.icons.append(icon)
        self.myExtraInfos.append(prompt)
        # self.flowLayout.addWidget(card)
        

    def setSelectedIcon(self, icon: FluentIcon):
        """ set selected icon """
        index = self.icons.index(icon)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(False)

        self.currentIndex = index
        self.cards[index].setSelected(True)
        self.infoPanel.setIcon(icon,self.myExtraInfos[index])
        
    def __setQss(self):
        self.view.setObjectName('iconView')
        self.scrollWidget.setObjectName('scrollWidget')
        self.iconLibraryLabel.setObjectName('iconLibraryLabel')

        StyleSheet.ICON_INTERFACE.apply(self)

        if self.currentIndex >= 0:
            self.cards[self.currentIndex].setSelected(True, True)
                
    def search(self, keyWord: str):
        """ search icons """
        keyWord = keyWord.lower()  # 将搜索词转为小写
        # if(keyWord==""):
        #     self.showAllIcons()
        #     return
        self.flowLayout.removeAllWidgets()  # 移除FlowLayout中的所有部件
        self.flowLayout.update()  # 更新FlowLayout
        for card in self.cards:  
            # 假设card对象有一个name属性代表图标的名字，如果没有，应该替换为合适的属性
            isVisible = keyWord in card.prompt['title'].lower() 
            card.setVisible(isVisible)
            if isVisible:
                self.flowLayout.addWidget(card)
                self.flowLayout.update()

                
    def showAllIcons(self):
        self.flowLayout.removeAllWidgets()
        self.flowLayout.update()
        for card in self.cards:
            self.flowLayout.addWidget(card)
            self.flowLayout.update()
            card.show()
            self.flowLayout.update()
            # size = self.size()       
            # self.resize(size.width() + 1, size.height())  # 少量改变窗口大小
            # self.resize(size)  # 立即将其改回  
          


class IconInterface(GalleryInterface):
    """ Icon interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.icons,
            subtitle="",
            parent=parent
        )

        self.iconView = IconCardView(self)
        self.vBoxLayout.addWidget(self.iconView)
