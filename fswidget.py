
from typing import Optional
from fnmatch import fnmatch
from PyQt6 import QtWidgets, QtCore


class TreeItem(QtWidgets.QTreeWidgetItem):

    def __init__(self, info: QtCore.QFileInfo):
        super().__init__([info.fileName()])
        self.info = info


class FSWidget(QtWidgets.QTreeWidget):
    """
    Widget used to display file tree with exclusions
    Every method that returns QTreeWidgetItem will now have a attribute 'info' of type QFileInfo
    """

    def __init__(self, root_path: str, exclude_patterns: Optional[list[str]] = None):
        """
        ### Parameters
        root_path: str
            Path to the root directory
        exclude_patterns: Optional[list[str]]
            A list of glob patterns used to determine if to view a directory
        """
        super().__init__()
        self.root_path = root_path
        self.exclude_patterns = exclude_patterns
        self.icon_provider = QtWidgets.QFileIconProvider()
        self.setHeaderHidden(True)
        self.addTopLevelItems(self._generate_tree(self.root_path))

    def is_excluded(self, dirpath: str) -> bool:
        # checks if the path is to be excluded or not
        if self.exclude_patterns:
            return any(fnmatch(dirpath, pattern) for pattern in self.exclude_patterns)
        return False

    def reset(self) -> None:
        # resets the tree and repopulates it with fresh data
        self.clear()
        self.addTopLevelItems(self._generate_tree(self.root_path))
        
    def load_icons(self) -> None:
        # displays correct icon in tree items
        ## use it after changing the icon_provider attribute
        iterator = QtWidgets.QTreeWidgetItemIterator(self)
        while iterator.value():
            item: TreeItem = iterator.value()
            item.setIcon(0, self.icon_provider.icon(item.info))
            iterator += 1

    def _generate_tree(self, directory: str) -> list[TreeItem]:
        subdir_items: list[TreeItem] = []
        file_items: list[TreeItem] = []
        dir_iterator = QtCore.QDirIterator(directory)

        dir_iterator.next() # returns ''
        dir_iterator.next() # returns '.'
        dir_iterator.next() # returns '..'

        while dir_iterator.filePath():
            info = dir_iterator.fileInfo()
            tree_item = TreeItem(info)
            tree_item.setIcon(0, self.icon_provider.icon(info))
            
            if info.isDir():
                if not self.is_excluded(info.filePath()):
                    tree_item.addChildren(self._generate_tree(info.filePath()))
                    subdir_items.append(tree_item)
            else:
                file_items.append(tree_item)
            
            dir_iterator.next()

        subdir_items.sort(key=lambda item: item.info.fileName())
        file_items.sort(key=lambda item: item.info.fileName())
        return subdir_items + file_items


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        directory = sys.argv[1]
    else:
        directory = '.'

    app = QtWidgets.QApplication([])
    win = FSWidget(directory)
    win.resize(600, 300)
    win.show()
    app.exec()
