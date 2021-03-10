from PyQt5.QtWidgets import QMessageBox, QLineEdit


class FileEdit(QLineEdit):
    def __init__(self, parent):
        super(FileEdit, self).__init__(parent)

        self.setDragEnabled(True)

    def dragEnterEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls and urls[0].scheme() == 'file':
            filepath = str(urls[0].path())[1:]
            # Data Type
            if filepath[-4:].upper() == ".jpg":
                self.setText(filepath)
            else:
                dialog = QMessageBox()
                dialog.setWindowTitle("Error: Invalid File")
                dialog.setText("Only .jpg files are accepted")
                dialog.setIcon(QMessageBox.Warning)
                dialog.exec_()
