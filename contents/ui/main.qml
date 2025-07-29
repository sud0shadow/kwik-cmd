import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import org.kde.plasma.plasmoid 2.0
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 3.0 as PlasmaComponents3
import "../code/config_manager.js"
as ConfigManager
import "../code/command_executor.js"
as CommandExecutor

PlasmoidItem {
    id: root

    property
    var commands: []
    property string statusMessage: "Ready"
    property int selectedIndex: -1

    Layout.minimumWidth: 400
    Layout.minimumHeight: 350
    Layout.preferredWidth: 500
    Layout.preferredHeight: 400

    Component.onCompleted: {
        loadCommands()
    }

    function loadCommands() {
        commands = ConfigManager.loadCommands()
        statusMessage = "Loaded " + commands.length + " commands"
        selectedIndex = -1
    }

    function saveCommands() {
        var error = ConfigManager.saveCommands(commands)
        if (error) {
            statusMessage = error
        } else {
            statusMessage = "Commands saved successfully"
        }
    }

    function runSelectedCommand() {
        if (selectedIndex >= 0 && selectedIndex < commands.length) {
            var command = commands[selectedIndex]
            statusMessage = "Running: " + command.name

            CommandExecutor.executeCommand(command.command, function (stdout, stderr) {
                if (stderr) {
                    statusMessage = stderr
                } else {
                    statusMessage = "Command ran successfully!\n" + (stdout || "")
                }
            })
        } else {
            statusMessage = "Please select a valid command!"
        }
    }

    function addNewCommand() {
        var name = newNameField.text.trim()
        var command = newCommandField.text.trim()

        if (name && command) {
            var newCommand = {
                "name": name,
                "command": command
            }
            commands.push(newCommand)
            commands = commands.slice() // Trigger binding update
            saveCommands()

            newNameField.text = ""
            newCommandField.text = ""
            statusMessage = "New command '" + name + "' added successfully!"
        } else {
            statusMessage = "Please fill in both fields to add a command."
        }
    }

    function updateCommand() {
        var name = newNameField.text.trim()
        var command = newCommandField.text.trim()

        if (selectedIndex >= 0 && selectedIndex < commands.length && name && command) {
            var oldName = commands[selectedIndex].name
            commands[selectedIndex].name = name
            commands[selectedIndex].command = command
            commands = commands.slice() // Trigger binding update
            saveCommands()

            newNameField.text = ""
            newCommandField.text = ""
            statusMessage = "Command '" + oldName + "' updated successfully!"
        } else {
            statusMessage = "Please select a command and fill in the fields to update."
        }
    }

    function deleteCommand() {
        if (selectedIndex >= 0 && selectedIndex < commands.length) {
            var commandName = commands[selectedIndex].name
            commands.splice(selectedIndex, 1)
            commands = commands.slice() // Trigger binding update
            saveCommands()

            selectedIndex = -1
            newNameField.text = ""
            newCommandField.text = ""
            statusMessage = "Command '" + commandName + "' deleted successfully!"
        } else {
            statusMessage = "Please select a valid command to delete."
        }
    }

    fullRepresentation: ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // Header
        PlasmaComponents3.Label {
            text: "KDE Command Executor"
            font.bold: true
            font.pointSize: 14
            Layout.alignment: Qt.AlignHCenter
        }

        // Status message
        PlasmaComponents3.Label {
            id: statusLabel
            text: root.statusMessage
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            Layout.maximumHeight: 60
            background: Rectangle {
                color: theme.backgroundColor
                border.color: theme.textColor
                border.width: 1
                radius: 4
            }
            padding: 5
        }

        // Command selection
        RowLayout {
            Layout.fillWidth: true

            PlasmaComponents3.Label {
                text: "Select Command:"
            }

            PlasmaComponents3.ComboBox {
                id: commandCombo
                Layout.fillWidth: true
                model: root.commands.map(function (cmd) { return cmd.name })

                onCurrentIndexChanged: {
                    root.selectedIndex = currentIndex
                    if (currentIndex >= 0 && currentIndex < root.commands.length) {
                        // Pre-fill form fields when selecting a command
                        newNameField.text = root.commands[currentIndex].name
                        newCommandField.text = root.commands[currentIndex].command
                    }
                }
            }
        }

        // Action buttons
        RowLayout {
            Layout.fillWidth: true
            spacing: 5

            PlasmaComponents3.Button {
                text: "Run Command"
                Layout.fillWidth: true
                onClicked: root.runSelectedCommand()
                enabled: root.selectedIndex >= 0
            }

            PlasmaComponents3.Button {
                text: "Update Command"
                Layout.fillWidth: true
                onClicked: root.updateCommand()
                enabled: root.selectedIndex >= 0
            }

            PlasmaComponents3.Button {
                text: "Delete Command"
                Layout.fillWidth: true
                onClicked: root.deleteCommand()
                enabled: root.selectedIndex >= 0
            }
        }

        // Separator
        Rectangle {
            Layout.fillWidth: true
            height: 1
            color: theme.textColor
            opacity: 0.3
        }

        // Add/Edit form
        GridLayout {
            Layout.fillWidth: true
            columns: 2
            columnSpacing: 10
            rowSpacing: 5

            PlasmaComponents3.Label {
                text: "Command Name:"
            }

            PlasmaComponents3.TextField {
                id: newNameField
                Layout.fillWidth: true
                placeholderText: "Enter command name..."
            }

            PlasmaComponents3.Label {
                text: "Command:"
            }

            PlasmaComponents3.TextField {
                id: newCommandField
                Layout.fillWidth: true
                placeholderText: "Enter shell command..."
            }
        }

        PlasmaComponents3.Button {
            text: "Add New Command"
            Layout.alignment: Qt.AlignHCenter
            onClicked: root.addNewCommand()
        }

        // Reload button
        PlasmaComponents3.Button {
            text: "Reload Commands"
            Layout.alignment: Qt.AlignHCenter
            onClicked: root.loadCommands()
        }
    }

    compactRepresentation: PlasmaComponents3.Button {
        text: "CMD"
        onClicked: root.expanded = !root.expanded

        ToolTip.visible: hovered
        ToolTip.text: "Quick Command Executor\nCommands: " + root.commands.length
    }
}