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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, 'blender_paths.json')

    try:
        with open(json_path, 'r') as file:
            template_paths = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"{translate('Error reading blender_paths.json: ', 'Ошибка при чтении blender_paths.json:')} {e}")
        return None

    possible_paths = []

    # Проверяем на всех дисках
    print(f"{translate('Checking possible Blender paths on all drives...', 'Проверка возможных путей Blender на всех дисках...')}")
    for drive in [f"{chr(letter)}:/" for letter in range(65, 91) if os.path.exists(f"{chr(letter)}:/")]:
        for template in template_paths:
            template = template.replace("/", "\\") if "nt" in os.name else template
            for i in range(2, 10):
                for j in range(1, 10):
                    version = f"{i}.{j}"
                    if os.path.isabs(template):
                        if os.path.exists(template.replace("<version>", version)):
                            possible_paths.append((template.replace('<version>', version), 'Steam' if 'Steam' in template else 'Alternate'))
                    else:
                        path = os.path.join(drive, template.replace("<version>", version))
                        if os.path.exists(path):
                            possible_paths.append((path, 'Steam' if 'Steam' in template else 'Alternate'))

    # Проверка в домашней директории (Linux)
    home_dir = str(Path.home())
    for template in template_paths:
        if template.startswith("/") or template.startswith("."):
            path = os.path.join(home_dir, template.replace("<version>", version))
            if os.path.exists(path):
                possible_paths.append((path, 'Steam' if 'Steam' in template else 'Alternate'))

    possible_paths = list(set(possible_paths))  # Убираем дубли

    if not possible_paths:
        print(translate('Blender not found. Please enter the path manually.', 'Blender не найден. Пожалуйста, введите путь вручную.'))
        while True:
            manual_path = input(translate("Enter the full path to the Blender folder: ", "Введите полный путь к папке Blender: "))
            if os.path.exists(manual_path):
                possible_paths.append((manual_path, 'Manual'))
                if get_user_input(translate("Do you want to add this path to the list of Blender paths?", "Вы хотите добавить этот путь в список путей Blender?"), ["yes", "no"]) == "yes":
                    add_to_json(manual_path)
                break
            else:
                print(translate("The path does not exist. Please try again.", "Путь не существует. Попробуйте снова."))

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
        self.aces_combo.addItems(["PixelManager", "1.3 Pro"])
        self.layout.addWidget(self.aces_combo)

        # Execute Button
        self.execute_button = QPushButton(translate("Execute", "Выполнить"))
        self.execute_button.clicked.connect(self.execute)
        self.layout.addWidget(self.execute_button)

        # Status Label
        self.status_label = QLabel(translate("Status: Ready", "Статус: Готово"))
        self.layout.addWidget(self.status_label)

    def specify_custom_path(self):
        custom_path = QFileDialog.getExistingDirectory(self, translate("Select Blender Folder", "Выберите папку Blender"))
        if custom_path:
            self.version_combo.addItem(f"{custom_path} - Manual")

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
        try:
            mode = self.mode_combo.currentText()
            selected_version = self.version_combo.currentText()

            if not selected_version or " - " not in selected_version:
                QMessageBox.critical(self, translate("Error", "Ошибка"),
                                        translate("Invalid Blender version selected.", "Выбрана недействительная версия Blender."))
                return

            aces_version = self.aces_combo.currentText()

            blender_datafiles_path = selected_version.split(" - ")[0]
            backup_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), blender_datafiles_path.split(os.sep)[-3])
            aces_base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), aces_version)

            if mode == translate("Installation", "Установка"):
                self.create_backup(blender_datafiles_path, backup_dir)
                self.install_aces(blender_datafiles_path, aces_base_path)
            elif mode == translate("Uninstallation", "Удаление"):
                self.uninstall_aces(blender_datafiles_path, backup_dir)

            QMessageBox.information(self, translate("Success", "Успех"),
                                        translate("Operation completed successfully.", "Операция успешно завершена."))
        except Exception as e:
            print(f"An error occurred: {e}")
            QMessageBox.critical(self, translate("Error", "Ошибка"),
                                 translate(f"An error occurred: {e}", f"Произошла ошибка: {e}"))
            input("Press Enter to exit...")

    def create_backup(self, blender_datafiles_path, backup_dir):
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
            shutil.copytree(blender_datafiles_path, backup_dir, dirs_exist_ok=True)

    def install_aces(self, blender_datafiles_path, aces_path):
        if not os.path.exists(aces_path):
            raise FileNotFoundError(translate("ACES folder not found.", "Папка ACES не найдена."))

        for file in os.listdir(blender_datafiles_path):
            file_path = os.path.join(blender_datafiles_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        shutil.copytree(aces_path, blender_datafiles_path, dirs_exist_ok=True)

    def uninstall_aces(self, blender_datafiles_path, backup_dir):

        if not os.path.exists(backup_dir):
            raise FileNotFoundError(translate("Backup folder not found.", "Папка резервной копии не найдена."))

        for file in os.listdir(blender_datafiles_path):
            file_path = os.path.join(blender_datafiles_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        shutil.copytree(backup_dir, blender_datafiles_path, dirs_exist_ok=True)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    window = BlenderACESInstaller()
    window.show()
    sys.exit(app.exec())
