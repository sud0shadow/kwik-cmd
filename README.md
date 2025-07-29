# **QuickCmd: KDE Command Executor Widget**

QuickCmd is a **KDE Plasma widget** designed to let you quickly run, manage, and store custom shell commands right from your desktop panel. Whether you're a developer, sysadmin, or a power user, QuickCmd will help you execute commands and manage tasks efficiently with just a few clicks.

---

## 🚀 **Installation**

### 1. **Install Dependencies**

Before running QuickCmd, ensure you have the required dependencies installed on your system:

```bash
sudo apt update
sudo apt install python3 python3-pyqt5
```

### 2. **Clone the Repository**

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/QuickCmd.git
cd QuickCmd
```

### 3. **Install Plasma SDK (for KDE Widgets)**

To develop Plasma widgets, you need to install the Plasma SDK if it's not already installed:

```bash
sudo apt install plasma-sdk
```

### 4. **Run the Widget**

Simply run the widget by executing the following command:

```bash
python3 main.py
```

This will launch the **KDE Command Executor** widget on your desktop.

---

## ⚙️ **Usage**

### 1. **Run Commands**

You can quickly run commands by selecting one from the dropdown menu and clicking the **Run Command** button. The selected command will be executed directly from your panel.

### 2. **Add New Commands**

- Enter the **Command Name** and the **Command** in the provided fields.
- Click **Add New Command** to add it to the list.
- The new command will be saved in a JSON configuration file and can be executed instantly.

### 3. **Update Commands**

- To update an existing command, select it from the dropdown, enter the new details, and click **Update Command**.
- The command will be updated in the configuration file automatically.

### 4. **Delete Commands**

- Select the command you want to delete from the dropdown.
- Click **Delete Command**, and it will be removed from the panel and configuration.

### 5. **Persistent Storage**

All commands are saved in a `commands_config.json` file, so your commands will persist even after you close the widget.

---

## 🔧 **Configuration File**

QuickCmd stores all the commands you add in a JSON file called `commands_config.json` located in the project directory.

Here’s an example of how the file looks:

```json
{
  "commands": [
    {
      "name": "List Files",
      "command": "ls -l"
    },
    {
      "name": "Update System",
      "command": "sudo apt update && sudo apt upgrade"
    }
  ]
}
```

---

## 🎨 **Customization**

QuickCmd is customizable, and you can easily modify the commands, layout, or even extend it with more functionality. Here’s what you can do:

- **Modify Command Names and Commands**: Edit the `commands_config.json` file directly to change existing commands.
- **Change the UI**: Customize the widget’s interface by modifying the `kde_widget.py` file. You can adjust layouts, labels, or even add new functionalities to enhance the app.

---

## 📜 **License**

QuickCmd is licensed under the **MIT License**.

---

## 🌟 **Contributing**

Feel free to fork this repository and create pull requests with your improvements. If you have any feature requests, open an issue, and we’ll look into it!

---

## 🤖 **Support**

For any questions or issues, please open an issue on GitHub, and I’ll be happy to help. You can also reach out directly via email or the repository discussions section.

---

**Happy Commanding!** ✨
