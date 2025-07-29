import subprocess

class CommandExecutor:
    @staticmethod
    def execute_command(command):
        """Execute the selected shell command."""
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()

            if process.returncode == 0:
                return output.decode()
            else:
                return f"Error: {error.decode()}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
