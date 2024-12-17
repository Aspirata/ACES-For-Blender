import os
import shutil
import sys
import locale

def get_input(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(get_localized_message("Invalid input. Possible options: ", "Неверный ввод. Возможные варианты: ") ,valid_options)

def get_localized_message(message_en, message_ru, *args):
    system_language = locale.getlocale()[0]
    if system_language == 'Russian_Russia':
        return message_ru
    else:
        return message_en

def find_blender_path(version):
    potential_paths = []
    system = sys.platform
    
    if "win" in system:
        drives = [f"{chr(d)}:\\" for d in range(65, 91) if os.path.exists(f"{chr(d)}:\\")]
        universal_blender_path = os.path.join(version, "datafiles", "colormanagement")

        for drive in drives:
            steam_path = os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common", "Blender", universal_blender_path)
            foundation_path = os.path.join(drive, "Program Files", "Blender Foundation", f"Blender {version}", universal_blender_path)

            if os.path.exists(steam_path):
                potential_paths.append(steam_path)
            if os.path.exists(foundation_path):
                potential_paths.append(foundation_path)
    
    else:
        home_dir = os.path.expanduser("~")
        blender_base_path = os.path.join(home_dir, "blender", universal_blender_path)

        blender_paths = [
            os.path.join("/opt", "blender", universal_blender_path),
            os.path.join(home_dir, "blender", universal_blender_path),
            os.path.join(home_dir, ".steam", "steamapps", "common", "Blender", universal_blender_path),
        ]
        
        for path in blender_paths:
            if os.path.exists(path):
                potential_paths.append(path)

    if potential_paths:
        if len(potential_paths) > 1:
            print(get_localized_message("Multiple Blender installations found:", "Найдено несколько установок Blender: "))
            for idx, path in enumerate(potential_paths, 1):
                print(f"{idx}. {path}")
            choice = get_input(get_localized_message("Choose the number of the correct path: ", "Выберите номер нужного пути: "), [str(i) for i in range(1, len(potential_paths) + 1)])
            return potential_paths[int(choice) - 1]
        return potential_paths[0]

    return None

aces_versions = {"1.2": "ACES 1.2", "1.3": "ACES 1.3 Pro"}
aces_version = get_input(get_localized_message("Select the ACES version for installation (1.2 or 1.3): ", "Выберите версию ACES для установки (1.2 или 1.3): "), aces_versions.keys())

blender_version = get_input(get_localized_message("Enter Blender version (e.g., 2.8, 3.5, 4.4): ", "Введите версию Blender (например, 2.8, 3.5, 4.4): "), [f"{x}.{y}" for x in range(2, 5) for y in range(0, 5)])

blender_path = find_blender_path(blender_version)
if not blender_path:
    blender_path = os.path.join(get_input(get_localized_message("Enter the path to Blender folder manually: ", "Укажите путь до папки Blender вручную: ")), blender_version, "datafiles", "colormanagement")

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
aces_folder = os.path.join(script_dir, aces_versions[aces_version])
backup_folder = os.path.join(script_dir, f"{blender_version}")

if not os.path.exists(aces_folder):
    print(get_localized_message("Error: ACES folder not found. Ensure it exists in the script directory.", "Ошибка: Папка с ACES не найдена. Убедитесь, что она существует в директории скрипта."))

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
    print(get_localized_message("Starting to copy Blender Colorspace files...", "Начинается копирование файлов Blender Colorspace..."))

    for item in os.listdir(blender_path):
        item_path = os.path.join(blender_path, item)
        backup_item_path = os.path.join(backup_folder, item)
        
        if os.path.isfile(item_path):
            shutil.copy2(item_path, backup_item_path)
        elif os.path.isdir(item_path):
            shutil.copytree(item_path, backup_item_path)

    print(get_localized_message("Old files successfully backed up and deleted.", "Старые файлы успешно скопированы и удалены."))
else:
    print(get_localized_message("Backup folder already exists. Skipping backup.", "Папка резервного копирования уже существует. Пропускаем создание резервной копии."))

print(get_localized_message("Starting to delete old files from Blender folder...", "Начинается удаление старых файлов из папки Blender..."))
for item in os.listdir(blender_path):
    item_path = os.path.join(blender_path, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

shutil.copytree(aces_folder, blender_path, dirs_exist_ok=True)
print(get_localized_message("ACES successfully installed", "ACES успешно установлена"))

input(get_localized_message("Press Enter to exit the program.", "Нажмите Enter, чтобы завершить работу программы."))
