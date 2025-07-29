import sys
import subprocess
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QLineEdit, QFormLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class KDEWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize the label early to be able to display error messages
        self.label = QLabel("Initializing...", self)

        # Ensure the config file exists
        self.config_file = "commands_config.json"
        if not self.config_exists():
            self.create_config_file()

        # Load commands from the config file
        self.commands = self.load_commands()

        # Setting up the UI
        self.setWindowTitle("KDE Command Executor")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        # Label to show status
        layout.addWidget(self.label)

        # Combo box for selecting an option
        self.combo = QComboBox(self)
        self.populate_combo_box()
        layout.addWidget(self.combo)

        # Buttons for CRUD operations
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

        # Layout for adding new command
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

    def config_exists(self):
        """Check if the config file exists."""
        try:
            with open(self.config_file, 'r') as file:
                pass
            return True
        except FileNotFoundError:
            return False

    def create_config_file(self):
        """Create the config file if it doesn't exist."""
        initial_data = {"commands": []}
        try:
            with open(self.config_file, "w") as file:
                json.dump(initial_data, file, indent=4)
        except Exception as e:
            self.label.setText(f"Error creating the config file: {str(e)}")

    def load_commands(self):
        """Load commands from the JSON config file."""
        try:
            with open(self.config_file, "r") as file:
                data = json.load(file)
                return data["commands"]
        except Exception as e:
            self.label.setText(f"Error loading commands: {str(e)}")
            return []

    def save_commands(self):
        """Save the updated commands to the config file."""
        try:
            with open(self.config_file, "w") as file:
                json.dump({"commands": self.commands}, file, indent=4)
        except Exception as e:
            self.label.setText(f"Error saving the commands: {str(e)}")

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
            self.execute_command(command_data["command"])
        else:
            self.label.setText("Please select a valid option!")

    def execute_command(self, command):
        """Execute the selected shell command."""
        try:
            # Run the command
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()

            if process.returncode == 0:
                self.label.setText(f"Command ran successfully!\n{output.decode()}")
            else:
                self.label.setText(f"Error: {error.decode()}")
        except Exception as e:
            self.label.setText(f"An error occurred: {str(e)}")

    def add_new_command(self):
        """Add a new command to the config file."""
        new_name = self.new_name.text()
        new_command = self.new_command.text()

        if new_name and new_command:
            new_command_data = {"name": new_name, "command": new_command}
            self.commands.append(new_command_data)
            self.combo.addItem(new_name)

            # Update the config file with the new command
            self.save_commands()

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

                # Update the UI and save the changes
                self.populate_combo_box()
                self.save_commands()

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

                # Update the UI and save the changes
                self.populate_combo_box()
                self.save_commands()

                self.new_name.clear()
                self.new_command.clear()
                self.label.setText(f"Command '{selected_option}' deleted successfully!")
            else:
                self.label.setText(f"Command '{selected_option}' not found!")
        else:
            self.label.setText("Please select a valid command to delete.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = KDEWidget()
    widget.show()
    sys.exit(app.exec_())
