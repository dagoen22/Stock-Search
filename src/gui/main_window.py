import sys
import logging

from PyQt5.QtWidgets import (
    QMainWindow,
    QTableView,
    QLabel,
    QAction,
    QMenuBar,
    QMenu,
    QPushButton,
    QFileDialog,
)

from PyQt5.QtCore import Qt, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super(TableModel, self).__init__()
        self._data = data
        self._headers = headers

    def data(self, index, role):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return str(self._data[i][self._headers[j]])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]


class MainWindow(QMainWindow):
    def __init__(self, data, headers):
        super().__init__()
        logging.info("Iniciando metodo principal")

        self.setWindowTitle("Consultor de Mercado")
        self.resize(800, 600)
        table_model = TableModel(data, headers)
        table_view = QTableView()
        table_view.setModel(table_model)
        self.setCentralWidget(table_view)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save_data)
        self.addToolBarBreak()
        self.addToolBar(Qt.BottomToolBarArea, self.create_toolbar([save_button]))

        self.createActions()
        self.createMenuBar()

    def createMenuBar(self):
        menuBar = QMenuBar(self)
        file_menu = QMenu("&Arquivo", self)
        file_menu.triggered.connect(self.save_data)
        file_menu.addAction(self.saveAction)
        menuBar.addMenu(file_menu)
        self.setMenuBar(menuBar)

    def create_toolbar(self, buttons):
        toolbar = self.addToolBar("Save Toolbar")
        for button in buttons:
            toolbar.addWidget(button)
        return toolbar

    def createActions(self):
        self.saveAction = QAction("&Salvar", self)

    def save_data(self):
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "CSV files (*.csv)"
            )
            if file_path:
                with open(file_path, "w") as file:
                    headers = [
                        header.replace(" ", "_").lower() for header in self.headers
                    ]
                    file.write(",".join(headers) + "\n")
                    logging.info("Salvando arquivo")
                    for row in self.data:
                        values = [str(row.get(header, "")) for header in headers]
                        file.write(",".join(values) + "\n")
                    logging.info("Arquivo salvo com sucesso")
        except Exception as e:
            logging.error("erro ao salvar arquivo", e)


class LoadingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tela de Carregamento")
        self.resize(800, 600)
