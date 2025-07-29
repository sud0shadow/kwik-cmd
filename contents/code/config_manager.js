.pragma library

var Qt = globalThis.Qt;

function getConfigPath() {
    // Get the plasmoid's data directory
    var dataDir = Qt.resolvedUrl("../../").toString().replace("file://", "");
    return dataDir + "commands_config.json";
}

function configExists() {
    var configPath = getConfigPath();
    var file = Qt.createQmlObject('import QtQuick 2.0; import Qt.labs.platform 1.0; FileInfo { }', Qt.application);
    file.filePath = configPath;
    return file.exists;
}

function createConfigFile() {
    var configPath = getConfigPath();
    var initialData = {
        "commands": []
    };
    
    try {
        var request = new XMLHttpRequest();
        request.open("PUT", "file://" + configPath, false);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(JSON.stringify(initialData, null, 4));
        return null;
    } catch (e) {
        return "Error creating config file: " + e.toString();
    }
}

function loadCommands() {
    var configPath = getConfigPath();
    
    if (!configExists()) {
        createConfigFile();
        return [];
    }
    
    try {
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "file://" + configPath, false);
        xhr.send();
        
        if (xhr.status === 200 || xhr.status === 0) {
            var data = JSON.parse(xhr.responseText);
            return data.commands || [];
        }
    } catch (e) {
        console.log("Error loading commands:", e);
        return [];
    }
    return [];
}

function saveCommands(commands) {
    var configPath = getConfigPath();
    var data = {
        "commands": commands
    };
    
    try {
        var request = new XMLHttpRequest();
        request.open("PUT", "file://" + configPath, false);
        request.setRequestHeader('Content-Type', 'application/json');
        request.send(JSON.stringify(data, null, 4));
        return null;
    } catch (e) {
        return "Error saving commands: " + e.toString();
    }
}