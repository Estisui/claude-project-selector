import os
import shutil
import json
import pyperclip

# JavaScript code to copy to clipboard
js_code = '''
function clickRemoveButtons() {
  const buttons = Array.from(document.querySelectorAll('button[aria-label="Remove from project knowledge"]'));
  buttons.sort((a, b) => {
    const rectA = a.getBoundingClientRect();
    const rectB = b.getBoundingClientRect();
    return rectB.top - rectA.top;
  });
  buttons.forEach((button, index) => {
    setTimeout(() => {
      button.click();
      console.log(`Clicked button ${index + 1} of ${buttons.length}`);
    }, index * 100);
  });
}
clickRemoveButtons();
'''

# Config file to read the last used folders
config_file = 'app_config.json'

def empty_folder(folder):
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
        print(f"Папка '{folder}' очищена.")
    else:
        print(f"Папка '{folder}' не существует.")

def copy_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            # Skip .h files
            if file.endswith('.h'):
                print(f"Ignoring file: {file}")
                continue
            
            source_path = os.path.join(root, file)
            destination_path = os.path.join(destination_folder, file)
            counter = 1
            while os.path.exists(destination_path):
                name, ext = os.path.splitext(file)
                destination_path = os.path.join(destination_folder, f"{name}_{counter}{ext}")
                counter += 1
            shutil.copy2(source_path, destination_path)
            print(f"Скопирован файл: {destination_path}")

def run_copy_files_and_js():
    """Function to automatically run the file copy and JS copying process based on saved config."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
            source_folder = config.get('input_folder', '')
            destination_folder = config.get('output_folder', '')

            if source_folder and destination_folder:
                print(f"Copying files from {source_folder} to {destination_folder}")
                empty_folder(destination_folder)
                copy_files(source_folder, destination_folder)

                # Copy JS code to clipboard
                pyperclip.copy(js_code)
                print("JS code copied to clipboard!")
            else:
                print("Source or destination folder not set. Please run the GUI to configure folders.")
    else:
        print("No configuration file found. Please run the GUI to set the folders.")

if __name__ == '__main__':
    run_copy_files_and_js()
