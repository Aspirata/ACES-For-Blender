import os
import shutil
import locale

def get_input(prompt, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if valid_options is None or user_input in valid_options:
            return user_input
        print(get_localized_message("Invalid input. Possible options: ", ["Invalid input. Possible options: "], valid_options))

def get_localized_message(message_en, message_ru, *args):
    system_language = locale.getdefaultlocale()[0]
    if system_language == 'ru_RU':
        return message_ru[0].format(*args)
    else:
        return message_en.format(*args)

blender_version_prompt = get_localized_message("Enter Blender version (e.g., 2.8, 3.5, 4.4): ", ["Введите версию Blender (например, 2.8, 3.5, 4.4): "])
blender_version = get_input(blender_version_prompt, [f"{x}.{y}" for x in range(2, 5) for y in range(0, 5)])

universal_blender_path = os.path.join(blender_version, "datafiles", "colormanagement")
blender_path = os.path.join("/usr/share/steam/steamapps/common/Blender", universal_blender_path)
alternate_blender_path = os.path.join(f"/opt/blender/{blender_version}", universal_blender_path)

if not os.path.exists(blender_path) and not os.path.exists(alternate_blender_path):
    error_message = get_localized_message("Error: The specified Blender version ({}) was not found.", ["Ошибка: Указанная версия Blender ({}) не найдена.", blender_version])
    print(error_message)
    blender_path = os.path.join(get_input(get_localized_message("Enter the path to Blender folder manually (e.g., /home/user/Blender/4.3): ", ["Укажите путь до папки Blender вручную (например, /home/user/Blender/4.3): "])), universal_blender_path)
elif os.path.exists(blender_path) and os.path.exists(alternate_blender_path):
    choice_prompt = get_localized_message("Multiple paths found, choose one (Steam or Alt): ", ["Найдено несколько путей, выберите один из (Steam или Alt): "])
    choice = get_input(choice_prompt, ["Steam", "Alt"])
    blender_path = blender_path if choice == "Steam" else alternate_blender_path
else:
    blender_path = blender_path if os.path.exists(blender_path) else alternate_blender_path

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
backup_folder = os.path.join(script_dir, f"{blender_version}")

if not os.path.exists(backup_folder):
    error_message = get_localized_message("Error: Backup folder for Blender {} not found: {}", ["Ошибка: Резервная папка для Blender {} не найдена: {}", backup_folder])
    print(error_message)
else:
    print(get_localized_message("Starting Installation, don't close the window", "Запуск Установки, не закрывайте окно"))
    try:
        for item in os.listdir(blender_path):
            item_path = os.path.join(blender_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        success_message = get_localized_message("ACES files in Blender folder successfully deleted.", ["Файлы ACES в папке Blender успешно удалены."])
        print(success_message)

        for item in os.listdir(backup_folder):
            backup_item_path = os.path.join(backup_folder, item)
            blender_item_path = os.path.join(blender_path, item)
            if os.path.isfile(backup_item_path):
                shutil.copy2(backup_item_path, blender_item_path)
            elif os.path.isdir(backup_item_path):
                shutil.copytree(backup_item_path, blender_item_path, dirs_exist_ok=True)
        success_message_restore = get_localized_message("Files successfully restored from backup folder {}", ["Файлы успешно восстановлены из резервной папки {}.", backup_folder])
        print(success_message_restore)
    except Exception as e:
        error_message = get_localized_message("Error restoring files: {}", ["Ошибка при восстановлении файлов: {}", e])
        print(error_message)

input_message = get_localized_message("Press Enter to exit the program.", ["Нажмите Enter, чтобы завершить работу программы."])
input(input_message)
