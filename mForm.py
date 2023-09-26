from newForm import *

g_img = np.array([])
fn = 0
mark = 0
pos_s = [0, 0] 
pos_e = [0, 0]
pre_len = 0
mark1 = 0
cmap = ''

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('main studio')
        self.resize(820, 660)
        self.ui()
        # self.colorBtn()
        # self.sizeBtn()
        self.scaled_img = None
        self.menubar_file()
        self.edit_process()
        self.menubar_image_process()
        self.filter_process()
        self.menubar_recognize_process()
        self.img = []
        self.t_filename = 0
        self.img_w = 0
        self.img_h = 0
        self.arr_t_filename = ['init']
        self.redo_time = 1
        self.undo_time = 1
        self.file_pos = 0

    def ui(self):
        self.cur_t_filename = -1
        self.last_x, self.last_y = None, None
        self.penSize = 10
        self.penColor = QColor('#000000')
        self.img = np.zeros([600, 800, 3], np.uint8)+255
        cv2.imwrite('temp/init.jpg', self.img)
        
            
        self.label = QLabel(self)
        self.label.setGeometry(10, 40, 800, 600)
        
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.showImage()
        
        self.warning = QLabel(self)
        self.warning.setGeometry(600, 5, 200, 30)
        self.warning.setStyleSheet('color:red')
        self.warning.setText('')

        self.text1 = QLabel(self)
        self.text1.setGeometry(500, 5, 200, 30)
        self.text1.setStyleSheet('color:blue')
        self.text1.setText('')
  
    def menubar_file(self):
        font = QFont()                       
        font.setFamily('Verdana')                  
        font.setPointSize(10)                      
        self.mbox = QMessageBox(self)
        self.menubar = QMenuBar(self)
        self.menu_file = QMenu('檔案')
        self.mbox.setFont(font)
        self.action_new = QAction('開新檔案')
        self.action_new.triggered.connect(self.newFile)
        self.menu_file.addAction(self.action_new)
        self.action_old = QAction('開起舊檔')
        self.action_old.triggered.connect(self.oldFile)
        self.menu_file.addAction(self.action_old)
        self.action_save = QAction('另存新檔')
        self.menu_file.addAction(self.action_save)
        self.action_save.triggered.connect(self.saveFile)
        self.action_close = QAction('關閉')
        self.menu_file.addAction(self.action_close)
        self.action_close.triggered.connect(self.closeFile)
        self.menubar.addMenu(self.menu_file)

    def newFile(self):
        self.cleanText()
        ret = self.mbox.question(self, 'question', '確定開新檔案？')
        if ret == self.mbox.Yes:
            self.canvas.fill(QColor('#ffffff'))
            self.label.setPixmap(self.canvas)
        else:
            return
    
    def oldFile(self):
        self.cleanText()
        filePath , filetype = QFileDialog.getOpenFileName(filter='IMAGE(*.jpg *.png)')
        if filePath: 
            arr = filePath.split('/')
            self.img = cv2.imread(arr[-2]+'/'+arr[-1])
            print(self.img.shape)
            
            self.showImage()
            self.saveImage()
            # self.update()
        try:
            if self.img.shape[0]>600 or self.img.shape[1]>800:
                self.warning.setText('此圖片大過版面，建議調整圖片尺寸')
                self.warning.adjustSize()
        except:
            pass
           
    def saveFile(self):
        self.cleanText()
        filePath, filterType = QFileDialog.getSaveFileName(self, '另存新檔', '', 'JPG(*.jpg);;(*.png)')  
        self.label.pixmap().save(filePath,'JPG',90)  

    def closeFile(self):
        # os.remove
        self.close()

    def edit_process(self):
        self.menu_edit = QMenu('編輯')

        self.redo = QAction('上一步')
        self.redo.triggered.connect(self.redoImage)
        self.menu_edit.addAction(self.redo)

        self.undo = QAction('復原')
        self.undo.triggered.connect(self.undoImage)
        self.menu_edit.addAction(self.undo)
        
        self.menubar.addMenu(self.menu_edit)

    def redoImage(self):
        global pre_len
        self.cleanText()
        l = len(self.arr_t_filename)
        
        if l-1-self.redo_time<0:
            self.warning.setText('無法回到上一步')
            return
        
        if pre_len!=l:
            self.arr_t_filename = self.arr_t_filename[:self.file_pos+1] + self.arr_t_filename[self.file_pos+self.redo_time:]
            self.redo_time = 1
        l = len(self.arr_t_filename)
        self.file_pos = l-1-self.redo_time
        self.img = cv2.imread('temp/'+self.arr_t_filename[self.file_pos]+'.jpg')
        self.showImage()
        
        self.redo_time+=1
        pre_len = l
        # print(self.redo_time, self.undo_time, self.file_pos)
        
    def undoImage(self):
        self.cleanText()
        l = len(self.arr_t_filename)
    
        if self.file_pos+self.undo_time == l or l == 0:
            self.warning.setText('無法復原圖片')
            return
        self.file_pos += self.undo_time
        self.img = cv2.imread('temp/'+self.arr_t_filename[self.file_pos]+'.jpg')
        self.showImage()
        if self.redo_time>1:
            self.redo_time-=1
        # print(self.redo_time, self.undo_time, self.file_pos)
        

    def menubar_image_process(self):
        
        self.menu_image = QMenu('圖像')

        self.gray = QAction('灰階')
        self.gray.triggered.connect(self.grayImage)
        self.menu_image.addAction(self.gray)

        self.map = QAction('尺寸調整')
        self.map.triggered.connect(self.adjustMap)
        self.menu_image.addAction(self.map)
        
        self.rotation = QMenu('旋轉')

        self.myrotation = QAction('自訂旋轉')
        self.myrotation.triggered.connect(self.rotationImage)

        self.h_flip = QAction('水平翻轉')
        self.h_flip.triggered.connect(self.horizonFlip)

        self.v_flip = QAction('垂直翻轉')
        self.v_flip.triggered.connect(self.verticalFlip)

        self.rotation.addActions([self.myrotation, self.h_flip, self.v_flip])
        self.menu_image.addMenu(self.rotation)

        self.retrieve = QAction('擷取')
        self.retrieve.triggered.connect(self.retrieveImage)
        self.menu_image.addAction(self.retrieve)

        self.cmap = QMenu('圖譜')

        self.spring = QAction('spring')
        self.spring.triggered.connect(self.cmapSpring)

        self.summer = QAction('summer')
        self.summer.triggered.connect(self.cmapSummer)

        self.autumn = QAction('autumn')
        self.autumn.triggered.connect(self.cmapAutumn)

        self.winter = QAction('winter')
        self.winter.triggered.connect(self.cmapWinter)

        self.bone = QAction('bone')
        self.bone.triggered.connect(self.cmapBone)

        self.cool = QAction('cool')
        self.cool.triggered.connect(self.cmapCool)

        self.copper = QAction('copper')
        self.copper.triggered.connect(self.cmapCopper)

        self.flag = QAction('flag')
        self.flag.triggered.connect(self.cmapFlag)

        self.hot = QAction('hot')
        self.hot.triggered.connect(self.cmapHot)

        self.inferno = QAction('inferno')
        self.inferno.triggered.connect(self.cmapInferno)

        self.cmap.addActions([self.spring, self.summer, self.autumn, self.winter, self.bone, self.cool, self.copper, self.flag, self.hot, self.inferno])
        self.menu_image.addMenu(self.cmap)
        
        self.contrast = QAction('對比')
        self.contrast.triggered.connect(self.contrastImage)
        self.menu_image.addAction(self.contrast)

        self.bright = QAction('調亮')
        self.bright.triggered.connect(self.brightImage)
        self.menu_image.addAction(self.bright)

        self.dark = QAction('調暗')
        self.dark.triggered.connect(self.darkImage)
        self.menu_image.addAction(self.dark)

        self.menubar.addMenu(self.menu_image)

    def grayImage(self):
        self.cleanText()
        try:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
            self.showImage()
            self.saveImage()
        except:
            self.warning.setText('此功能無法重複操作')
        
    def rotationImage(self):
        self.rf = RotationImageForm()
        self.rf.show()              
        self.rf.move(1450, 160)  
        self.rf.cfm_btn0.clicked.connect(self.rotationProcess)
        
    def rotationProcess(self):
        self.cleanText()
        try:
            d = int(self.rf.rtn_ipt.text())
            s = float(self.rf.scale_ipt.text())
            height, width = self.img.shape[:2]
            M = cv2.getRotationMatrix2D((width/2, height/2), d, s)
            img2 = cv2.warpAffine(self.img, M, (width, height))
            self.img = img2
            self.showImage()
            self.saveImage()
            self.rf.close()
        except:
            self.rf.error.setText('輸入內容有誤')

    def horizonFlip(self):
        self.cleanText()
        img1 = cv2.flip(self.img, 1)
        self.img = img1
        self.showImage()
        self.saveImage()

    def verticalFlip(self):
        self.cleanText()
        img1 = cv2.flip(self.img, 0)
        self.img = img1
        self.showImage()
        self.saveImage()

    def adjustMap(self):
        self.cleanText()
        self.amf = AdjustMapImageForm()
        # print(self.img_h)
        self.amf.w_ipt.setText(str(self.img_w))
        self.amf.h_ipt.setText(str(self.img_h))
        self.amf.show()              
        self.amf.move(1450, 160)  
        self.amf.cfm_btn0.clicked.connect(self.adjustMapProcess)

    def adjustMapProcess(self):
        self.cleanText()
        try:
            w = int(self.amf.w_ipt.text())
            h = int(self.amf.h_ipt.text())
            img1 = cv2.resize(self.img, (w, h))
            self.img = img1
            self.showImage()
            self.saveImage()
            self.amf.close()
        except:
             self.amf.error.setText('輸入內容有誤')

    def retrieveImage(self):
        self.cleanText()
        global g_img
        global fn
        # self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        
        g_img = self.img
        fn = self.t_filename
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', retrieveImg)
        while(1):
            cv2.imshow('image', g_img)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()
        if str(self.t_filename) not in self.arr_t_filename:
            self.arr_t_filename.append(str(self.t_filename))
        self.cur_t_filename+=1
        self.t_filename+=1
        # print(self.t_filename)
        self.img = cv2.imread('./temp/'+str(fn)+'.jpg')
        self.showImage()

    def cmapSpring(self):
        self.cmap_ = 'spring'
        self.cmapStyle()

    def cmapSummer(self):
        self.cmap_ = 'summer'
        self.cmapStyle()

    def cmapAutumn(self):
        self.cmap_ = 'autumn'
        self.cmapStyle()
  
    def cmapWinter(self):
        self.cmap_ = 'winter'
        self.cmapStyle()

    def cmapBone(self):
        self.cmap_ = 'bone'
        self.cmapStyle()

    def cmapCool(self):
        self.cmap_ = 'cool'
        self.cmapStyle()

    def cmapCopper(self):
        self.cmap_ = 'copper'
        self.cmapStyle()

    def cmapFlag(self):
        self.cmap_ = 'flag'
        self.cmapStyle()

    def cmapHot(self):
        self.cmap_ = 'hot'
        self.cmapStyle()

    def cmapInferno(self):
        self.cmap_ = 'inferno'
        self.cmapStyle()
        
    def cmapStyle(self):
        self.cleanText()
        self.img =  cv2.imread('./temp/'+str(self.cur_t_filename)+'.jpg')
        self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        plt.imshow(self.img, cmap= self.cmap_)
        plt.axis('off')
        plt.savefig('./temp/'+str(self.cur_t_filename)+'_0'+'.jpg', bbox_inches='tight',pad_inches = 0)
        self.img = cv2.imread('./temp/'+str(self.cur_t_filename)+'_0'+'.jpg')
        img1 = cv2.resize(self.img, (self.img_w, self.img_h))
        self.img = img1
        self.showImage()
        cv2.imwrite('./temp/'+str(self.cur_t_filename)+'_0'+'.jpg',self.img)
        if str(self.cur_t_filename)+'_0' not in self.arr_t_filename:
            self.arr_t_filename.append(str(self.cur_t_filename)+'_0')

    def contrastImage(self):
        self.cif = ContrastImageForm()
        self.cif.show()              
        self.cif.move(1450, 160)  
        self.cif.cfm_btn0.clicked.connect(self.contrastProcess)

    def contrastProcess(self):
        self.cleanText()
        try:
            cont = int(self.cif.ct_ipt.text())
            bri = int(self.cif.b_ipt.text())
            img1 = self.img * (cont/127 + 1) - cont + bri
            # self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            cv2.imwrite('temp/'+str(self.t_filename)+'.jpg', img1)
            if str(self.t_filename) not in self.arr_t_filename:
                self.arr_t_filename.append(str(self.t_filename))
            self.cur_t_filename+=1
            self.t_filename+=1
            self.img = cv2.imread('temp/'+str(self.cur_t_filename)+'.jpg')
            self.showImage()
            self.cif.close()
            
        except:
            self.cif.error.setText('輸入內容有誤')

    def brightImage(self):
        self.cleanText()
        img1 = self.img
        print(len(img1))
        print(len(img1[0]))
        print(len(img1[0][0]))
        for i in range(len(img1)):
            for j in range(len(img1[i])):
                for k in range(len(img1[i][j])):
                    if img1[i][j][k]+20>255:
                        img1[i][j][k] == 255
                    else:
                        img1[i][j][k]+=20
        self.img = img1
        self.showImage()
        self.saveImage()
    
    def darkImage(self):
        self.cleanText()
        img1 = self.img
        for i in range(len(img1)):
            for j in range(len(img1[i])):
                for k in range(len(img1[i][j])):
                    if img1[i][j][k]-20<0:
                        img1[i][j][k] == 0
                    else:
                        img1[i][j][k]-=20
        self.img = img1
        self.showImage()
        self.saveImage()

    def filter_process(self):
        self.menu_filter = QMenu('濾鏡')
        
        self.contour = QMenu('輪廓')

        self.contourDetect = QAction('輪廓描繪')
        self.contourDetect.triggered.connect(self.contourDetectImage)

        self.contourGradient = QAction('一般輪廓')
        self.contourGradient.triggered.connect(self.contourGradientImage)
        self.contour.addActions([self.contourDetect, self.contourGradient])
        self.menu_filter.addMenu(self.contour)
        self.blur = QMenu('模糊')

        self.averblur = QAction('均值模糊')
        self.averblur.triggered.connect(self.averblurImage)

        self.rectblur = QAction('方框模糊')
        self.rectblur.triggered.connect(self.rectblurImage)

        self.medblur = QAction('中值模糊')
        self.medblur.triggered.connect(self.medblurImage)

        self.Gaussianblur = QAction('高斯模糊')
        self.Gaussianblur.triggered.connect(self.GaussianblurImage)

        self.blur.addActions([self.averblur, self.rectblur, self.medblur, self.Gaussianblur])
        self.menu_filter.addMenu(self.blur)

        self.sharp = QAction('銳利化')
        self.sharp.triggered.connect(self.sharpImage)
        self.menu_filter.addAction(self.sharp)

        self.erode = QAction('降低雜訊')
        self.erode.triggered.connect(self.erodeImage)
        self.menu_filter.addAction(self.erode)

        self.dilate = QAction('增加雜訊')
        self.dilate.triggered.connect(self.dilateImage)
        self.menu_filter.addAction(self.dilate)

        self.opening = QAction('開運算')
        self.opening.triggered.connect(self.openingImage)
        self.menu_filter.addAction(self.opening)

        self.closing= QAction('閉運算')
        self.closing.triggered.connect(self.closingImage)
        self.menu_filter.addAction(self.closing)

        self.menubar.addMenu(self.menu_filter)

    def contourDetectImage(self):
        self.cleanText()
        img1 = cv2.Canny(self.img, 50, 60)
        self.img = img1
        self.showImage()
        self.saveImage()

    def contourGradientImage(self):
        self.cleanText()
        kernel = np.ones((5, 5), np.uint8)
        img1 = cv2.morphologyEx(self.img, cv2.MORPH_GRADIENT, kernel)
        self.img = img1
        self.showImage()
        self.saveImage()

    def averblurImage(self):
        self.cleanText()
        self.aif = AverblurImageForm()
        self.aif.show()              
        self.aif.move(1450, 160)  
        self.aif.cfm_btn0.clicked.connect(self.averblurProcess)

    def averblurProcess(self):
        self.cleanText()
        try:
            intensity = int(self.aif.inte_ipt.text())
            img1 = cv2.blur(self.img, (intensity, intensity))
            self.img = img1
            self.showImage()
            self.saveImage()
            self.aif.close()
        except:
            self.aif.error.setText('輸入內容有誤')

    def rectblurImage(self):
        self.cleanText()
        self.rif = RectblurImageForm()
        self.rif.show()              
        self.rif.move(1450, 160)  
        self.rif.cfm_btn0.clicked.connect(self.rectblurProcess)

    def rectblurProcess(self):
        self.cleanText()
        try:
            intensity = int(self.rif.inte_ipt.text())
            img1 = cv2.boxFilter(self.img, -1, (intensity, intensity), normalize=0)
            self.img = img1
            self.showImage()
            self.saveImage()
            self.rif.close()
        except:
            self.rif.error.setText('輸入內容有誤')

    def medblurImage(self):
        self.cleanText()
        self.mif = MedblurImageForm()
        self.mif.show()              
        self.mif.move(1450, 160)  
        self.mif.cfm_btn0.clicked.connect(self.medblurProcess)

    def medblurProcess(self):
        self.cleanText()
        try:
            intensity = int(self.mif.inte_ipt.text())
            img1 = cv2.medianBlur(self.img, intensity)
            self.img = img1
            self.showImage()
            self.saveImage()
            self.mif.close()
        except:
            self.mif.error.setText('輸入內容有誤')
        
    def GaussianblurImage(self):
        self.cleanText()
        self.gif = GaussionblurImageForm()
        self.gif.show()              
        self.gif.move(1450, 160)  
        self.gif.cfm_btn0.clicked.connect(self.GaussionblurProcess)
    
    def GaussionblurProcess(self):
        self.cleanText()
        try:
            intensity = int(self.gif.inte_ipt.text())
            
            img1 = cv2.GaussianBlur(self.img, (intensity, intensity), 0, 0)
            self.img = img1
            self.showImage()
            self.saveImage()
            self.gif.close()
        except:
            self.gif.error.setText('輸入內容有誤')

    def sharpImage(self):
        self.cleanText()
        img1 = cv2.GaussianBlur(self.img, (0, 0),30)
        img2 = cv2.addWeighted( self.img, 1.5, img1, -0.5, 0)
        cv2.imwrite('temp/'+str(self.t_filename)+'.jpg',img2)
        self.img = cv2.imread('temp/'+str(self.t_filename)+'.jpg')
        self.showImage()
        self.t_filename+=1
        self.cur_t_filename+=1

    def erodeImage(self):
        self.cleanText()
        kernel = np.ones((3, 3), np.uint8)
        img1 = cv2.erode(self.img, kernel, iterations = 1)
        self.img = img1
        self.showImage()
        self.saveImage()    

    def dilateImage(self):
        self.cleanText()
        kernel = np.ones((3, 3), np.uint8)
        img1 = cv2.dilate(self.img, kernel, iterations = 1)
        self.img = img1
        self.showImage()
        self.saveImage()  

    def openingImage(self):
        self.cleanText()
        kernel = np.ones((5, 5), np.uint8)
        img1 = cv2.morphologyEx(self.img, cv2.MORPH_OPEN, kernel)
        self.img = img1
        self.showImage()
        self.saveImage()

    def closingImage(self):
        self.cleanText()
        kernel = np.ones((5, 5), np.uint8)
        img1 = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel)
        self.img = img1
        self.showImage()
        self.saveImage()

    def menubar_recognize_process(self):
        self.menu_recognize = QMenu('圖像辨識')

        self.face  = QAction('人臉')
        self.face.triggered.connect(self.faceRecog)
        self.menu_recognize.addAction(self.face)

        self.eyes  = QAction('眼睛')
        self.eyes.triggered.connect(self.eyesRecog)
        self.menu_recognize.addAction(self.eyes)

        self.carplate  = QAction('車牌')
        self.carplate.triggered.connect(self.carplateRecog)
        self.menu_recognize.addAction(self.carplate)

        self.QRcode  = QAction('QRcode')
        self.QRcode.triggered.connect(self.QRcodeRecog)
        self.menu_recognize.addAction(self.QRcode)

        self.menubar.addMenu(self.menu_recognize)

    def faceRecog(self):
        self.cleanText()
        img1 = self.img
        fc = cv2.CascadeClassifier('./model_data/haarcascade_frontalface_default.xml')
        faces = fc.detectMultiScale(img1, scaleFactor=1.15, minNeighbors=10, minSize=(1, 1))
        for (x, y, w, h) in faces:
            cv2.rectangle(img1, (x, y), (x+w, y+h), (0, 0, 255), 2)
        if len(faces) == 0:
            self.warning.setText('無法增測到人臉')
            return
           
        self.text1.setText('找到'+str(len(faces))+'張人臉')  
        self.img = img1
        self.showImage()
        self.saveImage()

    def eyesRecog(self):
        self.cleanText()
        img1 = self.img
        ey = cv2.CascadeClassifier('./model_data/haarcascade_eye.xml')
        eyes = ey.detectMultiScale(img1, scaleFactor=1.3, minNeighbors=20, minSize=(20, 20))
        
        for (x, y, w, h) in eyes:
            # cv2.imwrite('./face/face'+str(i)+'.jpg', img1[y:y+h, x:x+w])
            cv2.rectangle(img1, (x, y), (x+w, y+h), (255, 0, 0), 2)
        if len(eyes) == 0:
            self.warning.setText('無法增測到人的眼睛')
            return
        
        self.text1.setText('找到'+str(len(eyes)//2)+'雙眼睛')    
        self.img = img1
        self.showImage()
        self.saveImage()
    
    def carplateRecog(self):
        self.cleanText()
        img1 = self.img
        car_cascade = cv2.CascadeClassifier('model_data/haar_carplate.xml')
        plates = car_cascade.detectMultiScale(img1, scaleFactor=1.05, minNeighbors=3, minSize=(20,20), maxSize=(155, 50))

        if len(plates)>0:
            for (x, y, w, h) in plates:
                carplate = img1[y:y+h, x:x+w]

        else:
            self.warning.setText('偵測車牌失敗')
            return

        cv2.imwrite('./temp/car_plate.jpg', carplate)
        # print('車牌擷取完成')
        config = '--tessdata-dir "Tesseract-OCR\\tessdata"'
        pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR\\tesseract.exe'
        txt = pytesseract.image_to_string(Image.open('./temp/car_plate.jpg'), config = config)
        text = f'車牌號碼是:{txt}'
        self.text1.setText(text)
        self.text1.adjustSize()
        
        

    def QRcodeRecog(self):
        self.cleanText()
        qrcode=cv2.QRCodeDetector()
        data,bbox, rectified = qrcode.detectAndDecode(self.img)

        if bbox is not None:
            self.text1.setText(data)
            if data == '':
                self.warning.setText('找不到QRcode圖片')
                return
            try:
                chrome_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open_new(data)
            except:
                self.warning.setText('chrome路徑不符')
        else:
            self.warning.setText('找不到QRcode圖片')

    def showImage(self):
        try:
            img1 = self.img
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
            self.img_h, self.img_w, ch = img1.shape
            bytesPerline = self.img_w*ch
            qimg = QImage(img1, self.img_w, self.img_h, bytesPerline, QImage.Format_RGB888)
            self.canvas = QPixmap.fromImage(qimg)
            self.label.setPixmap(self.canvas)
            time.sleep(0.1)
        except:
            self.img_h, self.img_w = self.img.shape[:2]
            qimg = QImage(self.img, self.img_w, self.img_h, self.img.strides[0], QImage.Format_Indexed8)
            self.canvas = QPixmap.fromImage(qimg)
            self.label.setPixmap(self.canvas)
            time.sleep(0.1)

    def saveImage(self):
        cv2.imwrite('temp/'+str(self.t_filename)+'.jpg', self.img)
        if str(self.t_filename) not in self.arr_t_filename:
            self.arr_t_filename.append(str(self.t_filename))
        print(self.arr_t_filename)
        self.cur_t_filename+=1
        self.t_filename+=1
        self.warning.setText('')
        time.sleep(0.1)

    def cleanText(self):
        self.text1.setText('')
        self.warning.setText('')

def retrieveImg(event, x, y, flags, param):
    global g_img
    global mark
    global fn
    global pos_e
    global pos_s
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(mark)
        # print(x, y)
        if mark == 0:
            pos_s = [x, y]
            mark += 1
        elif mark == 1:
            pos_e = [x, y]
            img = g_img[min([pos_s[1], pos_e[1]]):max([pos_s[1], pos_e[1]]), min([pos_s[0], pos_e[0]]):max([pos_s[0], pos_e[0]])]
            # print(min(pos_s[1], pos_e[1]), max(pos_s[1], pos_e[1]), min(pos_s[0], pos_e[0]), max(pos_s[0], pos_e[0]))
            cv2.imwrite('./temp/'+str(fn)+'.jpg', img)
            mark = 0



