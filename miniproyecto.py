import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence #para añadir atajos
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
from markdown2 import Markdown 

file_path = None

app = QApplication([])
app.setApplicationName("KittyPad")

def dialogo_confirmacion():
    return QMessageBox.question(
        window, "Confirmación",
        "Tienes cambios sin guardar, ¿estás segur@?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save)

def save_if_modified():
    if text.document().isModified:
        answer = dialogo_confirmacion()
        if answer == QMessageBox.Save:
            guardar()
            return False
        elif answer == QMessageBox.Cancel:
            return False
    return True

class MyMainWindow(QMainWindow):
    def closeEvent(self, evt):
        if text.document().isModified():
            answer = dialogo_confirmacion()
            if answer == QMessageBox.Save:
                guardar()
            elif answer == QMessageBox.Cancel:
                evt.ignore()

window = MyMainWindow()
text = QPlainTextEdit()
window.setCentralWidget(text)
browser = QDockWidget()

barra_de_menus = window.menuBar()

menu_archivo = barra_de_menus.addMenu("&Archivo")

def nuevo():
    global file_path
    if save_if_modified:
        text.clear()
        webengine.markdown_to_html()
        file_path = None

accion_nuevo = QAction("&Nuevo")
accion_nuevo.setShortcut(QKeySequence.New)
accion_nuevo.triggered.connect(nuevo)
menu_archivo.addAction(accion_nuevo)

def mostrar_dialogo_abrir():
    global file_path
    if not save_if_modified:
        return
    filename, _ = QFileDialog.getOpenFileName(window,
                    "Abrir fichero...",
                    os.getcwd(),
                    "Ficheros de texto (*.txt, *.py, *.md)"
                    )
    if filename:
        with open(filename, "r") as f:
            text.setPlainText(f.read())
        file_path = filename
        webengine.markdown_to_html()

accion_abrir = QAction("&Abrir")
accion_abrir.setShortcut(QKeySequence.Open)
accion_abrir.triggered.connect(mostrar_dialogo_abrir)
menu_archivo.addAction(accion_abrir)

def guardar():
    if file_path:
        with open(file_path, "w") as f:
            f.write(text.toPlainText())
            webengine.markdown_to_html()
            text.document().setModified(False)
            print(text.document().isModified())
    else:
        mostrar_dialogo_guardar()

def mostrar_dialogo_guardar():
    global file_path  #porque dentro de la funcion hay otro espacio de nombres
    filename, _ = QFileDialog.getSaveFileName(window,
                    "Guardar fichero...",
                    os.getcwd(),
                    "Ficheros de texto (*.txt, *.py)"
                    )
    if filename:
        with open(filename, "w") as f:
            f.write(text.toPlainText())
        text.document().setModified(False)
        print(text.document().isModified())
        file_path = filename

accion_guardar = QAction("&Guardar")
accion_guardar.setShortcut(QKeySequence.Save)
accion_guardar.triggered.connect(guardar)
menu_archivo.addAction(accion_guardar)

accion_guardar_como = QAction("&Guardar como...")
accion_guardar_como.setShortcut(QKeySequence.SaveAs)
accion_guardar_como.triggered.connect(mostrar_dialogo_guardar)
menu_archivo.addAction(accion_guardar_como)

accion_cerrar = QAction("&Cerrar")
accion_cerrar.triggered.connect(window.close)
accion_cerrar.setShortcut(QKeySequence.Quit)
menu_archivo.addAction(accion_cerrar)

def mostrar_dialogo_acercade():
    text = """
    <center>
        <h2>KittyPad</h2>
        <img src="data:image/jpeg;base64,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">
    </center>
    <h4>Version 0.0.1</h4>
    <p>Copyright Miriam Anfaiha<//p>
    """
    QMessageBox.about(window, "Acerca de KittyPad...", text)

#Crear un menu "Ayuda"
menu_ayuda = barra_de_menus.addMenu("&Ayuda")
#Crear accion "Acerca de"
acerca_de = QAction("Acerca de...")
#Conectar signal triggered con mostrar_dialogo_acercade()
acerca_de.triggered.connect(mostrar_dialogo_acercade)
#Añadir acción a menú ayuda
menu_ayuda.addAction(acerca_de)


class MyMarkdownBrowser(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QWebEngineView()
        self.browser = QDockWidget("KittyBrowser", window)   
        dockwidget = self.browser
        dockwidget.setMinimumWidth(300)
        dockwidget.toggleViewAction()
        window.addDockWidget(Qt.RightDockWidgetArea, dockwidget)
        dockwidget.setWidget(self.view)

    def markdown_to_html(self):
        mkdown = Markdown()
        mk_text = text.toPlainText()
        markdown_converter = mkdown.convert(mk_text)
        self.view.setHtml(markdown_converter)

webengine = MyMarkdownBrowser()

menu_actualizar = barra_de_menus.addMenu("&Markdown a Html")
accion_actualizar = QAction("Actualizar")
accion_actualizar.setShortcut(QKeySequence.Refresh)
accion_actualizar.triggered.connect(webengine.markdown_to_html)
menu_actualizar.addAction(accion_actualizar)


class MyTreeView(QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))
        self.tree.doubleClicked.connect(self.open_file)
        dockwidget = QDockWidget("Explorador de archivos", window)
        dockwidget.setWidget(self.tree)
        dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        window.addDockWidget(Qt.LeftDockWidgetArea, dockwidget)
        barra_de_menus.addAction(dockwidget.toggleViewAction())


    def open_file(self):
        global file_path
        if not save_if_modified:
            return
        filename, _ = QFileDialog.getOpenFileName(window,
                    "Abrir fichero...",
                    os.getcwd(),
                    "Ficheros de texto (*.txt, *.py, *.md)"
                    )
        if filename:
            with open(filename, "r") as f:
                text.setPlainText(f.read())
            file_path = filename
            webengine.markdown_to_html()

file_explorer = MyTreeView()
files = QFileSystemModel()


window.show()
app.exec()