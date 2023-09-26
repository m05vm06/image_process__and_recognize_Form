from newForm import *

class AverblurImageForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('blur_control')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      

        self.lbl1 = QLabel(self)
        self.lbl1.setText('強度(R)')
        self.lbl1.move(25,50)
        self.lbl1.setFont(font)


        self.inte_ipt = QLineEdit(self)
        self.inte_ipt.move(80, 50)

        
        self.lbl3 = QLabel(self)
        self.lbl3.setText('建議奇數(uint)')
        self.lbl3.move(220,55)
        
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

class RectblurImageForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('blur_control')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      

        self.lbl1 = QLabel(self)
        self.lbl1.setText('強度(R)')
        self.lbl1.move(25,50)
        self.lbl1.setFont(font)


        self.inte_ipt = QLineEdit(self)
        self.inte_ipt.move(80, 50)

        
        self.lbl3 = QLabel(self)
        self.lbl3.setText('建議<5(uint<255)')
        self.lbl3.move(220,55)
        
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

class MedblurImageForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('blur_control')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      

        self.lbl1 = QLabel(self)
        self.lbl1.setText('強度(R)')
        self.lbl1.move(25,50)
        self.lbl1.setFont(font)


        self.inte_ipt = QLineEdit(self)
        self.inte_ipt.move(80, 50)

        
        self.lbl3 = QLabel(self)
        self.lbl3.setText('奇數(uint)')
        self.lbl3.move(220,55)
        
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

class GaussionblurImageForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('blur_control')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      

        self.lbl1 = QLabel(self)
        self.lbl1.setText('強度(R)')
        self.lbl1.move(25,50)
        self.lbl1.setFont(font)


        self.inte_ipt = QLineEdit(self)
        self.inte_ipt.move(80, 50)

        
        self.lbl3 = QLabel(self)
        self.lbl3.setText('奇數(uint)')
        self.lbl3.move(220,55)
        
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