
# PyQt based File System Widget

## Why

In QFileSystemModel you can not exclude a specific directory.

Here you can use glob patterns to stop a directory from showing
 
---

### Working

Uses QDirIterator to get files and directories inside a directory.

'fnmatch' module is used to check if a directory is excluded or not.

---

## Features and TODO
- [x] View a directory
- [x] Use glob patterns to stop a directory from showing
- [X] Lazy loading
- [ ] Watch for file changes

---

## Documentation

1. ### Creating instance of FSWidget
```python
root_path = 'path/to/directory'

# dont want anything that matches these to show
exclude_patterns = [
    '*/__pycache__',
    '*/dist',
    '*/env'
]

# loads the directory content when directory is expanded
## decreases startup time and memory usage for large directories
## by loading contents only when user wants it
lazy_loading = True

win = FSWidget(root_path, exclude_patterns, lazy_loading)
```

2. ### Using custom icons
```python
class CustomIconProvider(QtGui.QFileIconProvider):
    def icon(self, info: QtCore.QFileInfo) -> QtGui.QIcon:
        if info.suffix() in ('py', 'pyw'):
            return QtGui.QIcon('path/to/icon')
        return super().icon(info)

win = FSWidget(...)
win.icon_provider = CustomIconProvider()
win.load_icons() # necessary after changing icon provider
```
---
![](screenshot.jpg)
