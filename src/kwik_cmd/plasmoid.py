import sys
from PyQt5.QtWidgets import QApplication, QWidget
from kwik_cmd.kde_widget import KDEWidget  # Ensure this path is correct

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = KDEWidget()
    widget.show()
    sys.exit(app.exec_())
