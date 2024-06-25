from moduls import *
import password_check
import downloaders
import subprocess

# GitHub에서 최신 스크립트 다운로드 및 로드
subprocess.call(['python', 'downloaders.py'])


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('image_conversion.ui')
form_class = uic.loadUiType(form)[0]


# form_class = uic.loadUiType("test.ui")[0]


class MyWindow(QtWidgets.QMainWindow, QMessageBox, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # self.tab_2.setDisabled(True)
        self.pushButton_9.clicked.connect(self.password_check_btn)
        self.pushButton_3.clicked.connect(self.start_button)


    def password_check_btn(self):
        qqq = threading.Thread(target=password_check.password_check_run, args=(model,))
        qqq.start()

    def start_button(self):
        qqq = threading.Thread(target=downloaders.go_run, args=(model,))
        qqq.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = MyWindow()
    model.show()
    app.exec_()
    sys.exit(app.exec_())
