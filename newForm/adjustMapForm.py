from newForm import *

class AdjustMapImageForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AdjustMap_control')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      
       
        self.lbl1 = QLabel(self)
        self.lbl1.setText('寬度 : ')
        self.lbl1.move(60,50)
        self.lbl1.setFont(font)

        self.lbl2 = QLabel(self)
        self.lbl2.setText('高度 : ')
        self.lbl2.move(60, 80)
        self.lbl2.setFont(font)

        self.w_ipt = QLineEdit(self)
        self.w_ipt.move(100, 50)

        self.h_ipt = QLineEdit(self)
        self.h_ipt.move(100, 80)
        
        self.lbl3 = QLabel(self)
        self.lbl3.setText('px (uint)')
        self.lbl3.move(240,55)
        
        self.lbl4 = QLabel(self)
        self.lbl4.setText('px (uint)')
        self.lbl4.move(240, 85)

        self.error = QLabel(self)
        self.error.setText('')
        self.error.setGeometry(120, 20, 100, 25)
        self.error.setStyleSheet('color:red;')
        
        self.cfm_btn0 = QPushButton(self)
        self.cfm_btn0.setText('確認')
        self.cfm_btn0.setStyleSheet('font-size:16px;')
        self.cfm_btn0.setGeometry(40,130,100,40)
        
        self.cnl_btn0 = QPushButton(self)
        self.cnl_btn0.setText('取消')
        self.cnl_btn0.setStyleSheet('font-size:16px;')
        self.cnl_btn0.setGeometry(160,130,100,40) 
        self.cnl_btn0.clicked.connect(self.close)