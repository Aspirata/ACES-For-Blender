import os
import json
import shutil
from pathlib import Path
import locale

def translate(eng_text, ru_text):
    user_language = locale.getlocale()[0]
    return ru_text if 'Ru' in user_language else eng_text

# Получение входных данных от пользователя
def get_user_input(prompt, options=None):
    while True:
        user_input = input(f"{prompt}: ")
        if options and user_input not in options:
            print(f"{translate('Please select from: ', 'Пожалуйста, выберите из:')} {', '.join(options)}")
            continue
        return user_input

# Проверка путей Blender на всех доступных дисках
def find_blender_paths(version):
    script_dir = Path(__file__).parent
    json_path = script_dir / 'blender_paths.json'

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
            if os.path.isabs(template):  # Исключение для абсолютных путей
                if os.path.exists(template.replace("<version>", version)):
                    possible_paths.append(template.replace("<version>", version))
            else:
                path = os.path.join(drive, template.replace("<version>", version))
                if os.path.exists(path):
                    possible_paths.append(path)

    # Проверка в домашней директории (Linux)
    home_dir = str(Path.home())
    for template in template_paths:
        if template.startswith("/") or template.startswith("."):
            path = os.path.join(home_dir, template.replace("<version>", version))
            if os.path.exists(path):
                possible_paths.append(path)

    possible_paths = list(set(possible_paths))  # Убираем дубли

    if not possible_paths:
        print(translate('Blender not found. Please enter the path manually.', 'Blender не найден. Пожалуйста, введите путь вручную.'))
        while True:
            manual_path = input(translate("Enter the full path to the Blender folder: ", "Введите полный путь к папке Blender: "))
            if os.path.exists(manual_path):
                possible_paths.append(manual_path)
                if get_user_input(translate("Do you want to add this path to the list of Blender paths?", "Вы хотите добавить этот путь в список путей Blender?"), ["yes", "no"]) == "yes":
                    add_to_json(manual_path)
                break
            else:
                print(translate("The path does not exist. Please try again.", "Путь не существует. Попробуйте снова."))

    if len(possible_paths) > 1:
        print(translate("Found multiple Blender paths:", "Найдено несколько путей к Blender:"))
        for i, path in enumerate(possible_paths, start=1):
            print(f"{i}: {path}")
        choice = get_user_input(translate("Select the number of the Blender path: ", "Выберите номер пути к Blender: "), [str(i) for i in range(1, len(possible_paths) + 1)])
        return possible_paths[int(choice) - 1]

    return possible_paths[0]

# Добавление пути Blender в JSON
def add_to_json(path):
    script_dir = Path(__file__).parent
    json_path = script_dir / 'blender_paths.json'

    try:
        with open(json_path, 'r') as file:
            paths = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        paths = []

    if path not in paths:
        paths.append(path)
        with open(json_path, 'w') as file:
            json.dump(paths, file, indent=4)
        print(translate("Path added to blender_paths.json.", "Путь добавлен в blender_paths.json."))

# Создание бэкапа
def create_backup(blender_datafiles_path, blender_version):
    aces_parent_dir = Path(__file__).parent.parent
    backup_dir = aces_parent_dir / blender_version
    if not backup_dir.exists():
        print(f"{translate('Creating backup in', 'Создание резервной копии в')} {backup_dir}.")
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(blender_datafiles_path, backup_dir, dirs_exist_ok=True)
    else:
        print(translate("Backup already exists.", "Резервная копия уже существует."))

# Установка ACES
def install_aces(blender_datafiles_path, aces_path):
    if not os.path.exists(aces_path):
        print(translate("ACES folder not found. Check the location.", "Папка ACES не найдена. Проверьте расположение."))
        return

    print(translate("Deleting current color management files...", "Удаление текущих файлов управления цветом Blender..."))
    for file in os.listdir(blender_datafiles_path):
        file_path = os.path.join(blender_datafiles_path, file)
        if os.path.isfile(file_path) or os.path.isdir(file_path):
            shutil.rmtree(file_path) if os.path.isdir(file_path) else os.remove(file_path)

    print(translate("Copying ACES...", "Копирование ACES..."))
    shutil.copytree(aces_path, blender_datafiles_path, dirs_exist_ok=True)
    print(translate("ACES installation completed!", "Установка ACES завершена!"))

# Основной сценарий
def main():

    ACES_VERSIONS = json.load(open(Path(__file__).parent / 'aces_versions.json'))

    try:
        aces_version = ACES_VERSIONS[get_user_input(translate("ACES versions: \n1. 1.3 Pro \n2. PixelManager (Recommended) \nWhich version of ACES to install", "Версии ACES: \n1. 1.3 Pro \n2. PixelManager (Рекомендуется) \nКакую версию ACES установить"), ["1", "2"])]
        blender_version = get_user_input(translate("Specify the Blender version (e.g., 2.8, 3.6, 4.4)", "Укажите версию Blender (например, 2.8, 3.6, 4.4)"))

        blender_path = find_blender_paths(blender_version)
        if not blender_path:
            print(translate("Blender not found. Ensure the version is correct and try again.", "Blender не найден. Убедитесь, что версия указана правильно, и повторите попытку."))
            return

        blender_datafiles_path = Path(blender_path)

        if not blender_datafiles_path.exists():
            print(f"{translate('Folder', 'Папка')} {blender_datafiles_path} {translate('does not exist. Check the path.', 'не существует. Проверьте путь.')}")
            return

        aces_base_path = Path(__file__).parent.parent / aces_version

        create_backup(blender_datafiles_path, blender_version)
        install_aces(blender_datafiles_path, aces_base_path)

    except Exception as e:
        print(f"{translate('An error occurred: ', 'Произошла ошибка: ')}{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
