import string, sys, os, re, shutil
from ui_blender_aces_manager import *
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QTimer

def get_app_path() -> str:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS # .exe path
    else:
        return os.path.dirname(os.path.abspath(__file__)) # .py path

def find_blender_versions() -> list[str]:
    blender_paths = ["Program Files (x86)\\Steam\\steamapps\\common\\Blender", "SteamLibrary\\steamapps\\common\\Blender"]
    found_versions = []
    version_pattern = re.compile(r'^\d+\.\d+(\.\d+)?$')
    
    for drive_letter in string.ascii_uppercase:
        for blender_path in blender_paths:
            full_blender_path = os.path.join(f"{drive_letter}:\\", blender_path)
            if not os.path.exists(full_blender_path):
                continue

            for entry in os.listdir(full_blender_path):
                entry_path = os.path.join(full_blender_path, entry)
                if not os.path.isdir(entry_path):
                    continue
                
                colormanagement_path = os.path.join(entry_path, "datafiles", "colormanagement")
                if version_pattern.match(entry) and os.path.exists(colormanagement_path):
                    found_versions.append(colormanagement_path)

    return sorted(found_versions)

def find_aces_versions() -> list[str]:
    aces_path = os.path.join(get_app_path(), "ACES")
    aces_paths = os.listdir(aces_path)
    return sorted(aces_paths)

def create_colormanagement_backup(path: str) -> str:
    try:
        colormanagement_backup_path = os.path.join(os.path.dirname(path), f"{os.path.basename(path)}_backup")
        if os.path.exists(colormanagement_backup_path):
            return "Success"
        
        window.start_progress_animation("Создание бэкапа")
        shutil.copytree(path, colormanagement_backup_path)
        window.change_progress_status("Бэкап создан")
        return "Success"
    except Exception as e:
        print(str(e))
        return str(e)

def install_aces(blender_version_path: str, aces_version_path: str):
    try:
        window.start_progress_animation("Установка ACES")
        shutil.copytree(aces_version_path, blender_version_path, dirs_exist_ok=True)
        window.change_progress_status("ACES установлен")
        return "Success"
    except Exception as e:
        print(str(e))
        return str(e)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        global main_window
        main_window = self
        
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self._animate_dots)
        self.progress_text = ""
        self.dot_count = 0
        
        blender_versions = find_blender_versions()
        if blender_versions:
            blender_versions_default_index = blender_versions.index(blender_versions[-1])
            self.ui.blender_versions_combobox.addItems(blender_versions)
            self.ui.blender_versions_combobox.setCurrentIndex(blender_versions_default_index)

        self.ui.execute_button.clicked.connect(lambda: self.execute_aces(self.ui.blender_versions_combobox.currentText(), self.ui.aces_versions_combobox.currentText()))

        aces_versions = find_aces_versions()
        aces_versions_default_index = aces_versions.index(sorted(list(filter(lambda x: "pixelmanager" in x.lower(), aces_versions)))[-1])
        self.ui.aces_versions_combobox.addItems(aces_versions)
        self.ui.aces_versions_combobox.setCurrentIndex(aces_versions_default_index)
        
        self.ui.blender_versions_browse_button.clicked.connect(self.blender_versions_browse)
    
    def blender_versions_browse(self) -> str:
        colormanagement_path = QFileDialog.getExistingDirectory(self, "Выберите папку Blender Colormanagement")
        if not colormanagement_path:
            return "Fail"
        
        elif "colormanagement" not in colormanagement_path:
                QMessageBox.critical(
                    self,
                    "Ошибка",
                    f'Необходимо выбрать папку colormanagement, например "Blender\\5.0\\datafiles\\colormanagement"'
                )
                return "Fail"
        
        colormanagement_path = colormanagement_path.replace("/", "\\")
        if self.ui.blender_versions_combobox.findText(colormanagement_path) == -1:
            self.ui.blender_versions_combobox.addItem(colormanagement_path)
        
        self.ui.blender_versions_combobox.setCurrentText(colormanagement_path)
        return colormanagement_path

    def execute_aces(self, blender_version_path: str, aces_version_path: str) -> str:
        aces_version_path = os.path.join(get_app_path(), "ACES", aces_version_path)
        create_colormanagement_backup_result = create_colormanagement_backup(blender_version_path)
        if create_colormanagement_backup_result:
            QMessageBox.critical(
                self,
                "Ошибка",
                f'Неудалось создать бэкап: {create_colormanagement_backup_result}'
            )
            return "Fail"
        
        install_aces_result = install_aces(blender_version_path, aces_version_path)
        if install_aces_result:
            QMessageBox.critical(
                self,
                "Ошибка",
                f'Неудалось установить ACES: {install_aces_result}'
            )
            return "Fail"
        
        return "Success"

    def start_progress_animation(self, text: str) -> None:
        self.progress_text = text
        self.dot_count = 0
        self.progress_timer.start(500)
    
    def _animate_dots(self):
        self.dot_count = self.dot_count % 3 + 1
        self.ui.progress_label.setText(f"{self.progress_text}{'.' * self.dot_count}")
    
    def stop_progress_animation(self) -> None:
        self.progress_timer.stop()
        self.ui.progress_label.setText("")
    
    def change_progress_status(self, status: str) -> None:
        self.progress_timer.stop()
        self.ui.progress_label.setText(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())