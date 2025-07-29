.pragma library

var Qt = globalThis.Qt;

function executeCommand(command, callback) {
    var process = Qt.createQmlObject('
        import QtQuick 2.0
        import org.kde.plasma.core 2.0 as PlasmaCore
        
        PlasmaCore.DataSource {
            id: executable
            engine: "executable"
            connectedSources: []
            
            signal commandFinished(string stdout, string stderr, int exitCode)
            
            onNewData: {
                var stdout = data["stdout"] || ""
                var stderr = data["stderr"] || ""
                var exitCode = data["exit code"] || 0
                
                commandFinished(stdout, stderr, exitCode)
                disconnectSource(sourceName)
            }
        }
    ', Qt.application, "executable_" + Date.now());
    
    process.commandFinished.connect(function(stdout, stderr, exitCode) {
        if (exitCode === 0) {
            callback(stdout, null);
        } else {
            callback(null, "Error: " + stderr);
        }
        process.destroy();
    });
    
    process.connectSource(command);
}