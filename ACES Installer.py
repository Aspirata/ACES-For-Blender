import os
import sys
import json
import shutil
from pathlib import Path
import locale
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel,
                             QComboBox, QPushButton, QFileDialog, QMessageBox, QWidget)

def translate(eng_text, ru_text):
    user_language = locale.getlocale()[0]
    return ru_text if 'Ru' in user_language else eng_text

def find_blender_versions():
    script_dir = os.path.dirname(sys.executable)
    json_path = os.path.join(script_dir, 'blender_paths.json')

    if not os.path.exists(json_path):
        with open(json_path, "w") as file:
            json.dump(["Program Files (x86)/Steam/steamapps/common/Blender/<version>/datafiles/colormanagement","Program Files/Blender Foundation/Blender <version>/<version>/datafiles/colormanagement",
            "/opt/blender/<version>/datafiles/colormanagement","blender/<version>/<version>/datafiles/colormanagement",".steam/steamapps/common/Blender/<version>/datafiles/colormanagement"], file)
    try:
        with open(json_path, 'r') as file:
            template_paths = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"{translate('Error reading blender_paths.json: ', 'Ошибка при чтении blender_paths.json:')} {e}")
        return None

    possible_paths = []

    for drive in [f"{chr(letter)}:/" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:/")]:
        for template in template_paths:
            template = template.replace("/", os.sep) if "nt" in os.name else template
            for i in range(2, 10):
                for j in range(1, 10):
                    version = f"{i}.{j}"
                    if os.path.isabs(template):
                        path = os.path.normpath(template.replace("<version>", version))
                        if os.path.exists(path):
                            possible_paths.append((path, 'Steam' if 'Steam' in template else 'Alternate'))
                    else:
                        path = os.path.normpath(os.path.join(drive, template.replace("<version>", version)))
                        if os.path.exists(path):
                            possible_paths.append((path, 'Steam' if 'Steam' in template else 'Alternate'))

    # Проверка в домашней директории (Linux)
    home_dir = str(Path.home())
    for template in template_paths:
        if template.startswith("/") or template.startswith("."):
            path = os.path.normpath(os.path.join(home_dir, template.replace("<version>", version)))
            if os.path.exists(path):
                possible_paths.append((path, 'Steam' if 'Steam' in template else 'Alternate'))

    possible_paths = list(set(possible_paths))  # Убираем дубли

    return possible_paths

class BlenderACESInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(translate("Blender ACES Installer", "Установщик ACES для Blender"))
        self.setGeometry(300, 300, 300, 300)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.init_ui()

    def init_ui(self):
        # Mode Selection
        self.mode_label = QLabel(translate("Select mode:", "Выберите режим:"))
        self.layout.addWidget(self.mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([translate("Installation", "Установка"), translate("Uninstallation", "Удаление")])
        self.mode_combo.currentTextChanged.connect(self.disable_aces_version_combo)
        self.layout.addWidget(self.mode_combo)

        # Blender Version Selection
        self.version_label = QLabel(translate("Select Blender version:", "Выберите версию Blender:"))
        self.layout.addWidget(self.version_label)

        self.version_combo = QComboBox()
        self.populate_blender_versions()
        self.layout.addWidget(self.version_combo)

        # Custom Path Button
        self.custom_path_button = QPushButton(translate("Specify Custom Path", "Указать свой путь"))
        self.layout.addWidget(self.custom_path_button)
        self.custom_path_button.clicked.connect(self.specify_custom_path)
        
        # ACES Version Selection
        self.aces_label = QLabel(translate("Select ACES version:", "Выберите версию ACES:"))
        self.layout.addWidget(self.aces_label)

        self.aces_combo = QComboBox()
        self.aces_combo.addItems(["PixelManager", "ACES 1.3 Pro"])
        self.layout.addWidget(self.aces_combo)

        # Execute Button
        self.execute_button = QPushButton(translate("Execute", "Выполнить"))
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)
    
    def disable_aces_version_combo(self):
        if self.mode_combo.currentText() == translate("Uninstallation", "Удаление"):
            self.aces_combo.setEnabled(False)
        else:
            self.aces_combo.setEnabled(True)

    def specify_custom_path(self):
        while True:
            custom_path = os.path.normpath(QFileDialog.getExistingDirectory(self, translate("Select Blender Colormanagement Folder, for example C:/downloads/Blender 4.3/4.3/datafiles/colormanagement", 
                                                                                            "Выберите папку с colormanagement для Blender, например C:/downloads/Blender 4.3/4.3/datafiles/colormanagement")))
            
            if custom_path == "" or custom_path == ".":
                break
            elif "colormanagement" not in custom_path:
                QMessageBox.warning(self, translate("Error", "Ошибка"),
                                        translate("The specified path does not contain 'colormanagement' folder.", "Указанный путь не содержит папку 'colormanagement'."))
                continue

            if os.path.exists(custom_path):
                self.version_combo.addItem(f"{custom_path} - Manual")
                break
            else:
                QMessageBox.warning(self, translate("Error", "Ошибка"),
                                        translate("The specified path does not exist.", "Указанный путь не существует."))

    def populate_blender_versions(self):
        blender_versions = find_blender_versions()
        if blender_versions:
            for path, version in blender_versions:
                self.version_combo.addItem(f"{path} - {version}")
        else:
            QMessageBox.warning(self, translate("No Blender Versions Found", "Версии Blender не найдены"),
                                translate("No Blender installations found. Please specify the path manually.",
                                        "Установки Blender не найдены. Пожалуйста, укажите путь вручную."))
            self.specify_custom_path()

    def execute(self):
        mode = self.mode_combo.currentText()
        selected_version = self.version_combo.currentText()

        if not selected_version or " - " not in selected_version:
            QMessageBox.critical(self, translate("Error", "Ошибка"),
                                    translate("Invalid Blender version selected.", "Выбрана недействительная версия Blender."))
            return "Error"

        aces_version = self.aces_combo.currentText()
        script_dir = os.path.dirname(os.path.abspath(sys.executable))
        blender_datafiles_path = selected_version.split(" - ")[0]
        path_parts = blender_datafiles_path.split(os.sep)
        backup_dir = os.path.join(script_dir, path_parts[-3])

        aces_base_path = os.path.join(script_dir, aces_version)

        if mode == translate("Installation", "Установка"):
            backup_result = self.create_backup(blender_datafiles_path, backup_dir)
            if "Error" in backup_result:
                QMessageBox.critical(self, translate("Error", "Ошибка"), backup_result[1])
                return
            else:
                print(backup_result[1])

            aces_install_result = self.install_aces(blender_datafiles_path, aces_base_path)
            if "Error" in aces_install_result:
                QMessageBox.critical(self, translate("Error", "Ошибка"), aces_install_result[1])
                return
            else:
                print(aces_install_result[1])
        else:
            aces_uninstall_result = self.uninstall_aces(blender_datafiles_path, backup_dir)
            if "Error" in aces_uninstall_result:
                QMessageBox.warning(self, translate("Error", "Ошибка"), aces_uninstall_result[1])
                return
            else:
                print(aces_uninstall_result[1])

        QMessageBox.information(self, translate("Success", "Успех"),
                                translate("Operation completed successfully.", "Операция успешно завершена."))

    def create_backup(self, blender_datafiles_path, backup_dir):
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copytree(blender_datafiles_path, backup_dir, dirs_exist_ok=True)
            return ("Success", translate("Backup created successfully.", "Резервная копия успешно создана."))
        else:
            return ("Success", translate("Backup folder already exists.", "Папка резервной копии уже существует."))

    def install_aces(self, blender_datafiles_path, aces_path):
        if not os.path.exists(aces_path):
            return ("Error", translate("ACES folder not found.", "Папка ACES не найдена."))

        for file in os.listdir(blender_datafiles_path):
            file_path = os.path.join(blender_datafiles_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        shutil.copytree(aces_path, blender_datafiles_path, dirs_exist_ok=True)
        return ("Success", translate("ACES installed successfully.", "ACES успешно установлен."))

    def uninstall_aces(self, blender_datafiles_path, backup_dir):
        if not os.path.exists(backup_dir):
            return ("Error", translate("Backup folder not found.", "Папка резервной копии не найдена.") + "\n" + translate("Install ACES first.", "Сначала установите ACES."))
            
        for file in os.listdir(blender_datafiles_path):
            file_path = os.path.join(blender_datafiles_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        shutil.copytree(backup_dir, blender_datafiles_path, dirs_exist_ok=True)

        return ("Success", translate("ACES uninstalled successfully.", "ACES успешно удалён."))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = BlenderACESInstaller()
    window.show()
    sys.exit(app.exec())
