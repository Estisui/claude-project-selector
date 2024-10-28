import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QListWidget
from PyQt5.QtCore import Qt

# Config file to save the last used folders
config_file = 'app_config.json'

class HelperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_config()  # Load last used folders

    def initUI(self):
        self.setWindowTitle("Helper App")
        self.setGeometry(100, 100, 320, 400)

        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel('Helper App', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        layout.addWidget(title_label)

        layout.addSpacing(16)

        # Input Folders Selection
        self.input_folders_label = QLabel('Input Folders', self)
        layout.addWidget(self.input_folders_label)

        self.input_folders_list = QListWidget(self)
        layout.addWidget(self.input_folders_list)

        self.input_browse_button = QPushButton('Add Input Folder', self)
        self.input_browse_button.setObjectName("browse-button")
        self.input_browse_button.clicked.connect(self.add_input_folder)
        layout.addWidget(self.input_browse_button)

        self.remove_input_button = QPushButton('Remove Selected Folder', self)
        self.remove_input_button.clicked.connect(self.remove_selected_folder)
        layout.addWidget(self.remove_input_button)

        layout.addSpacing(16)

        # Output Folder Selection
        self.output_folder_label = QLabel('Output Folder', self)
        layout.addWidget(self.output_folder_label)

        self.output_folder_input = QLineEdit(self)
        self.output_folder_input.setPlaceholderText('/path/to/output')
        layout.addWidget(self.output_folder_input)

        self.output_browse_button = QPushButton('Browse', self)
        self.output_browse_button.setObjectName("browse-button")
        self.output_browse_button.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_browse_button)

        layout.addSpacing(16)

        # Save Button
        self.save_button = QPushButton('Save Configuration', self)
        self.save_button.setObjectName("save-button")
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        # Apply custom styles
        self.apply_styles()

    def apply_styles(self):
        """Apply QSS styles to the app."""
        qss_styles = '''
            QWidget {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f3f4f6;
                margin: 0;
                padding: 0;
            }

            QLabel {
                font-size: 14px;
                font-weight: 500;
                color: #4b5563;
            }

            QLineEdit {
                padding: 8px 12px;
                font-size: 14px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                outline: none;
            }

            QLineEdit:focus {
                border-color: #3b82f6;
            }

            QListWidget {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #d1d5db;
                border-radius: 4px;
            }

            QPushButton {
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 500;
                color: #ffffff;
                background-color: #3b82f6;
                border: none;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }

            QPushButton#browse-button {
                background-color: #ffffff;
                color: #4b5563;
                border: 1px solid #d1d5db;
            }

            QPushButton#browse-button:hover {
                background-color: #f3f4f6;
            }

            QPushButton#save-button {
                width: 100%;
                margin-top: 16px;
            }
        '''
        
        self.setStyleSheet(qss_styles)

    def add_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Input Folder')
        if folder:
            self.input_folders_list.addItem(folder)

    def remove_selected_folder(self):
        for item in self.input_folders_list.selectedItems():
            self.input_folders_list.takeItem(self.input_folders_list.row(item))

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Select Output Folder')
        if folder:
            self.output_folder_input.setText(folder)

    def load_config(self):
        """Load the last used folders from a config file."""
        
        if os.path.exists(config_file):
             with open(config_file, 'r') as file:
                 config = json.load(file)
                 input_folders = config.get('input_folders', [])
                 for folder in input_folders:
                     self.input_folders_list.addItem(folder)
                 self.output_folder_input.setText(config.get('output_folder', ''))

    def save_config(self):
         """Save the current input and output folders to a config file."""
         
         input_folders = [self.input_folders_list.item(i).text() for i in range(self.input_folders_list.count())]
         output_folder = self.output_folder_input.text()

         config = {
             'input_folders': input_folders,
             'output_folder': output_folder
         }

         with open(config_file, 'w') as file:
             json.dump(config, file, indent=4)

         print(f"Configuration saved: {config}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HelperApp()
    window.show()
    sys.exit(app.exec_())
