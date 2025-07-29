from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QFormLayout, QHBoxLayout
from config_manager import ConfigManager
from command_executor import CommandExecutor

class KDEWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Initializing...", self)
        self.config_manager = ConfigManager()
        
        if not self.config_manager.config_exists():
            self.config_manager.create_config_file()
        
        self.commands = self.config_manager.load_commands()

        self.setWindowTitle("KDE Command Executor")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.combo = QComboBox(self)
        self.populate_combo_box()
        layout.addWidget(self.combo)

        button_layout = QHBoxLayout()
        self.run_button = QPushButton("Run Command", self)
        self.run_button.clicked.connect(self.run_command)
        button_layout.addWidget(self.run_button)

        self.update_button = QPushButton("Update Command", self)
        self.update_button.clicked.connect(self.update_command)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Command", self)
        self.delete_button.clicked.connect(self.delete_command)
        button_layout.addWidget(self.delete_button)

        layout.addLayout(button_layout)

        form_layout = QFormLayout()
        self.new_name = QLineEdit(self)
        self.new_command = QLineEdit(self)
        self.add_button = QPushButton("Add New Command", self)

        form_layout.addRow("Command Name", self.new_name)
        form_layout.addRow("Command", self.new_command)
        form_layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_new_command)

        layout.addLayout(form_layout)

        self.setLayout(layout)

    def populate_combo_box(self):
        """Populate the combo box with the command names."""
        self.combo.clear()
        for cmd in self.commands:
            self.combo.addItem(cmd["name"])

    def run_command(self):
        """Run the selected command."""
        selected_option = self.combo.currentText()
        command_data = next((cmd for cmd in self.commands if cmd["name"] == selected_option), None)
        if command_data:
            output = CommandExecutor.execute_command(command_data["command"])
            self.label.setText(f"Command ran successfully!\n{output}")
        else:
            self.label.setText("Please select a valid option!")

    def add_new_command(self):
        """Add a new command to the config file."""
        new_name = self.new_name.text()
        new_command = self.new_command.text()
        if new_name and new_command:
            new_command_data = {"name": new_name, "command": new_command}
            self.commands.append(new_command_data)
            self.combo.addItem(new_name)
            self.config_manager.save_commands(self.commands)

            self.new_name.clear()
            self.new_command.clear()
            self.label.setText(f"New command '{new_name}' added successfully!")
        else:
            self.label.setText("Please fill in both fields to add a command.")

    def update_command(self):
        """Update the selected command."""
        selected_option = self.combo.currentText()
        updated_name = self.new_name.text()
        updated_command = self.new_command.text()

        if selected_option and updated_name and updated_command:
            command_data = next((cmd for cmd in self.commands if cmd["name"] == selected_option), None)
            if command_data:
                command_data["name"] = updated_name
                command_data["command"] = updated_command
                self.populate_combo_box()
                self.config_manager.save_commands(self.commands)

                self.new_name.clear()
                self.new_command.clear()
                self.label.setText(f"Command '{selected_option}' updated successfully!")
            else:
                self.label.setText(f"Command '{selected_option}' not found!")
        else:
            self.label.setText("Please fill in the fields to update the command.")

    def delete_command(self):
        """Delete the selected command."""
        selected_option = self.combo.currentText()

        if selected_option:
            command_data = next((cmd for cmd in self.commands if cmd["name"] == selected_option), None)

            if command_data:
                self.commands.remove(command_data)
                self.populate_combo_box()
                self.config_manager.save_commands(self.commands)

                self.new_name.clear()
                self.new_command.clear()
                self.label.setText(f"Command '{selected_option}' deleted successfully!")
            else:
                self.label.setText(f"Command '{selected_option}' not found!")
        else:
            self.label.setText("Please select a valid command to delete.")
