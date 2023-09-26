from newForm import *
from mForm import MainForm

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dir = os.getcwd()+'/temp'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    Form = MainForm()
    Form.show()
    sys.exit(app.exec_())
    
    