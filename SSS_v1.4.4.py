from PySide2.QtWidgets import QMainWindow, QApplication,QFileDialog
from PySide2.QtCore import QThread,Signal,Slot
from PySide2.QtGui import QPixmap,Qt

from SSSKW import Ui_MainWindow
import socket
from nptdms import TdmsWriter, ChannelObject,TdmsFile
import numpy as np
import time

def Socket_Connect(que,Dataque,pipe):
    client_Data = ""
    while True:
        if que.qsize() != 0:
            Data = que.get()
            if type(Data) == socket.socket:
                client_Data = Data
                try:
                    while True:
                        Send_Data = client_Data.recv(65536)
                        if Send_Data == b'ZZZZ\x14\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00':
                            continue
                        pipe.send(np.frombuffer(Send_Data,dtype="H")[84:])
                except Exception as e:
                    print(e)
                finally:
                    pipe.close()
                    client_Data.close()

def Socket_Send(que):
    client_Data = ""
    while True:
        if que.qsize() != 0:
            try:
                Data = que.get()
                if Data == "Close":
                    client_Data.close()
                elif type(Data) == socket.socket:
                    client_Data = Data
                else:
                    client_Data.send(Data)
            except Exception as e:
                print(e)
                client_Data.close()
                pass

def Save_File(que,proque):
    from time import ctime
    import re

    while True:
        if que.qsize() != 0:
            Save_Data = que.get()
            time_D = ctime()
            time_D = re.sub(" |:","_",time_D)

            path = './KW_CSV_SSSData/%s_DataKW.tdms'%time_D
            with TdmsWriter(path) as tdms_writer:
                for i in range(len(Save_Data)):
                    channel = ChannelObject('Sonar Data','Data %s'%i,Save_Data[i])
                    tdms_writer.write_segment([channel])
            
            proque.put("Done")

def Read_File(que,Data_Que):
    import time
    Data = 0
    Range = 0
    Step = 0.1
    while True:
        if que.qsize() != 0:
            Data_Read = que.get()
            if type(Data_Read) == list:
                Data = Data_Read[::-1]
                Range = 0
            elif type(Data_Read) == float:
                pass
            elif type(Data_Read) == int:
                Range = Data_Read
            elif Data_Read == 'Readit':
                while True:
                    try:
                        if que.qsize() != 0 :
                            Data_ = que.get()
                            if Data_ == 'Stop':
                                break
                            elif type(Data_) == float:
                                Step = Data_
                            elif type(Data_) == int:
                                Range = Data_
                        if len(Data) == Range:
                            break

                        Data_Que.put(Data[Range])
                        time.sleep(Step)
                        Range+=1
                    except Exception as e:
                        break

class Worker(QThread):
    Conn_S = Signal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.client = ""
        self.parent = parent

    def run(self):
        global IP, PORT,sock
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP,int(PORT)))
        sock.listen(1)

        try:
            while True:
                self.client, self.addr = sock.accept()
                self.parent.Check_NetworkConnection = True
                self.Conn_S.emit("NetWork Connected : {}".format(self.addr))
                que_recv.put(self.client)
                que_send.put(self.client)
        except Exception as e:
            pass
        finally:
            sock.close()

    def stop(self):
        if type(self.client) != str:
            self.client.close()
        sock.close()

class Worker2(QThread):
    Data_Send = Signal(list)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.cnt = 0
        self.Range_Speed = 0
        self.Range_Copy = 0

    def run(self):
        global Data_que,Data_List,Save_Data,lock,ZeroData,Read_que,b_pipe

        while True:
            if self.parent.Data_Read_Stop == False:
                try:
                    Data = b_pipe.recv()
                    if type(Data) == str:
                        Data_List.clear()
                    lock.acquire()
                    if self.parent.widget_2.height()==len(Data_List):
                        Data_List.pop()
                    lock.release()

                    if len(Data) == 0:
                        Data = ZeroData
                
                    self.Data_Send.emit(Data)

                    if self.parent.Read_File == False:
                        Data = np.where(np.array(Data)>255,255,np.array(Data).astype(np.uint8))
                        Save_Data.insert(0,Data)

                    Data_List.insert(0,Data)

                    if self.parent.Read_File == True:
                        self.cnt = self.parent.horizontalSlider.value()

                        self.cnt+=1

                        self.parent.label_18.setText("%i/%i"%(self.cnt,len(self.parent.Show_Image)))

                        if self.parent.comboBox_4.currentText() == "Step1":
                            self.Range_Speed = 0.15
                        elif self.parent.comboBox_4.currentText() == "Step2":
                            self.Range_Speed = 0.1
                        else:
                            self.Range_Speed = 0.07
                        
                        if self.Range_Speed != self.Range_Copy:
                            Read_que.put(self.Range_Speed)

                        self.Range_Copy = self.Range_Speed

                        self.parent.horizontalSlider.setValue(self.cnt)

                        if self.parent.horizontalSlider.maximum() == self.cnt:
                            self.cnt = 0
                            self.parent.Start_Data = False

                    if len(Data_List)!=0:

                        if self.parent.comboBox_3.currentText() == 'Color':
                            try:
                                img = applyColorMap(np.array(Data_List.copy()),COLORMAP_OCEAN)
                                img = resize(img,dsize=(self.parent.widget_2.width(),img.shape[0]),interpolation=INTER_AREA)
                                img_ = fromarray(img,'RGB')
                            except Exception as e:
                                Data_List.pop(0)
                        else:
                            img_ = fromarray(np.require(Data_List,np.int8,'C'),'L')
                except Exception as e:
                    # print(e)
                    continue
                finally:
                    qim = ImageQt(img_).copy()
                    self.image = QPixmap.fromImage(qim)
                    self.parent.label_15.setScaledContents(True)
                    self.parent.label_15.setPixmap(self.image)

class Worker3(QThread):
    D_Log = Signal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        global Progress_que,Data_List,Save_Data,lock
        while True:
            if Progress_que.qsize != 0:
                lock.acquire()
                Progress_Data = Progress_que.get()
                if Progress_Data == "Done":
                    Data_List.clear()
                    Save_Data.clear()
                    self.D_Log.emit("File Save Done")
                    lock.release()
                    break

class Worker4(QThread):
    Log_Send = Signal(str)
    AScope_Send = Signal(list)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        global Progress_que,Read_que
        try:
            channels_data = self.parent.tdms_file['Sonar Data'].channels()

            self.parent.Show_Image.clear()

            self.parent.horizontalSlider.setValue(0)

            for i in range(len(channels_data)):
                selected_data = self.parent.tdms_file['Sonar Data']['Data {}'.format(i)]
                self.parent.Show_Image.append(selected_data.data)
            self.Log_Send.emit("All Data Read")
            Read_que.put(self.parent.Show_Image)

            self.parent.horizontalSlider.setRange(0,len(self.parent.Show_Image))
            self.parent.label_18.setText("0/%i"%len(self.parent.Show_Image))

            self.parent.Data_Length = np.arange(-(len(self.parent.Show_Image[0])/100),len(self.parent.Show_Image[0])/100,0.02)

        except Exception as e:
            print(e)
            pass
    
    def ReadAll(self):
        Read_que.put("Readit")

class WindowClass(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._Worker = Worker(self)
        self._Worker2 = Worker2(self)
        self._Worker3 = Worker3(self)
        self._Worker4 = Worker4(self)

        # 버튼 동작
        self.pushButton.clicked.connect(self.NetWork_Start)
        self.pushButton_2.clicked.connect(self.NetWork_Stop)
        self.pushButton_6.clicked.connect(self.Scanning_Start)
        self.pushButton_5.clicked.connect(self.Scanning_Stop)
        self.splitter_3.splitterMoved.connect(self.split_move)
        self.splitter.splitterMoved.connect(self.split_move)
        self.pushButton_3.clicked.connect(self.FileOpen)
        self.pushButton_11.clicked.connect(self.Read_Save_Data)
        self.horizontalSlider.sliderReleased.connect(self.moving_Slider)
        self.pushButton_12.clicked.connect(self.Stop_Save_Data)

        # QThread 연동
        self._Worker.Conn_S.connect(self.Data_Log)
        self._Worker2.Data_Send.connect(self.Draw_AScope)
        self._Worker3.D_Log.connect(self.Data_Log)
        self._Worker4.Log_Send.connect(self.Data_Log)
        self._Worker4.AScope_Send.connect(self.Draw_AScope)

        # Thread 시작
        self._Worker2.start()

        #Widget 설정
        self.widget.getPlotItem().hideAxis('left')
        self.widget.getPlotItem().showGrid(x=True,y=True)

        #초기 값
        self.Data_Length = np.array([])
        self.pen = pyqtgraph.mkPen(color=(0,255,0),width=1)
        self.widget_Size = self.widget_2.height()
        self.widget_Size2 = self.widget_2.width()
        self.Read_File = False
        self.Show_Image = []
        self.Data_Read_Stop = False
        self.Start_NetWorking = False
        self.Start_Data = False
        self.Check_NetworkConnection = False

        if not os.path.exists('./KW_CSV_SSSData'):
                        os.makedirs('./KW_CSV_SSSData')

    def resizeEvent(self, event):

        global Data_List,lock
        lock.acquire()
        Data_List.clear()
        lock.release()

    def Stop_Save_Data(self):
        global Read_que,lock
        if self.Start_NetWorking == False:
            self.Data_Read_Stop = True
            self.Start_Data = False
            lock.acquire()
            Read_que.put("Stop")
            lock.release()

    def moving_Slider(self):
        global Read_que,lock,Data_que
        if self.Start_NetWorking == False:
            lock.acquire()
            self.label_18.setText("%i/%i"%(self.horizontalSlider.value(),len(self.Show_Image)))
            Read_que.put(self.horizontalSlider.value())
            Data_List.clear()
            lock.release()

    def split_move(self):
        global Data_List,lock
        lock.acquire()
        if (self.widget_Size != self.widget_2.height()) or (self.widget_Size2 != self.widget_2.width()):
            Data_List.clear()
            self.widget_Size = self.widget_2.height()
            self.widget_Size2 = self.widget_2.width()
        lock.release()

    def NetWork_Start(self):
        global IP, PORT
        # 시작 설정 값 
        IP = self.lineEdit_2.text()
        PORT = self.lineEdit.text()
        #

        self._Worker.start()
        self.Data_Log("NetWork Waiting")
    
    def NetWork_Stop(self):
        global Data_List
        self.Check_NetworkConnection = False
        Data_List.clear()
        que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
        que_send.put("Close")
        self._Worker.stop()
        self.Data_Log("NetWork Disconnected")

    def Scanning_Start(self):
        global Range,Gain,TVG,Pulse_Width,Save_que,ZeroData,Data_List,Save_Data,que_recv
        # 변수 선언
        if self.lineEdit_5.text() == '' or self.lineEdit_6.text() == '':
            self.MessageBox.about(self,'Alert','System Setting 값을 입력해주세요.')
        else:
            try:
                if self.Check_NetworkConnection == False:
                    self.MessageBox.about(self,'Alert','NetWork가 연결되어 있지 않습니다.')
                else:
                    if self.Start_Data == False:
                        self.Start_NetWorking = True
                        self.Data_Read_Stop = False
                        self.Read_File = False
                        self.Data_Length = np.arange(-int(self.lineEdit_5.text()),int(self.lineEdit_5.text()),0.02)
                        ZeroData = np.zeros(int(self.lineEdit_5.text())*100,dtype=np.uint8)
                        Range = b"\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x04\x00\x00\x00%s\x00\x00\x00\x00"%struct.pack("i",int(self.lineEdit_5.text()))
                        Gain = b"\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x05\x00\x00\x00%s\x00\x00\x00\x00"%struct.pack("i",int(self.lineEdit_6.text()))
                        TVG = b"\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x06\x00\x00\x00%s\x00\x00\x00\x00"%struct.pack("i",int(self.comboBox.currentIndex()))
                        Pulse_Width = b"\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x07\x00\x00\x00%s\x00\x00\x00\x00"%struct.pack("i",int(self.comboBox_2.currentIndex()))

                        Send_Data = [Range,Gain,TVG,Pulse_Width]
                        Data_List = []
                        Save_Data = []
                        que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

                        for i in Send_Data:
                            que_send.put(i)
                        
                        que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

                        self.Data_Log("System Start")
            except Exception as e:
                self.MessageBox.about(self,'Alert','잘못된 값을 입력하셨습니다.')

    def Scanning_Stop(self):
        global Data_List,Save_Data,Save_que
        if self.Start_Data == False:
            if self.Start_NetWorking == True:
                self.Data_Read_Stop = True
                self.Start_NetWorking = False
                que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
                if len(Save_Data)!=0:
                    Save_que.put(Save_Data)
                    time.sleep(0.5)
                    self._Worker3.start()

                self.Data_Log("System Stop")

    def FileOpen(self):
        global Data_List,Read_que
        if self.Start_NetWorking == True:
            self.MessageBox.about(self,'Alert','Stop버튼을 먼저 눌러주세요.')
        else:
            try:
                self.Read_File = True
                if Read_que.qsize != 0:
                    Read_que.put("Stop")
                    Data_List.clear()
                QFileName = QFileDialog.getOpenFileName(None,'Open File',"./")[0]
                self.tdms_file = TdmsFile(QFileName)
                self._Worker4.start()
            except Exception as e:
                pass

    @Slot(list)
    def Draw_AScope(self,AScope_Data):
        try:
            self.widget.setRange(xRange=[-(len(AScope_Data)/100),len(AScope_Data)/100],yRange=[-1,256],padding=0)
            self.widget.plot(self.Data_Length,AScope_Data,pen=self.pen,clear=True)

        except Exception:
            pass

    @Slot(str)
    def Data_Log(self,D_Log):
        self.textBrowser.append("{} : {}".format(ctime(),D_Log))

    def Read_Save_Data(self):
        global Data_List,Read_que
        if self.Start_NetWorking == False:
            if self.horizontalSlider.maximum() != self.horizontalSlider.value():
                self.Data_Read_Stop = False
                self.Start_Data = True
                self.Read_File = True
                Data_List.clear()
                self._Worker4.ReadAll()
                Read_que.put(self.horizontalSlider.value())


if __name__ == "__main__":
    import sys
    from multiprocessing import Queue,Process,freeze_support,Pipe
    import struct
    import pyqtgraph
    from PIL.Image import fromarray
    from PIL.ImageQt import ImageQt
    from cv2 import applyColorMap,resize,COLORMAP_OCEAN,INTER_AREA
    import os
    from time import ctime
    import time
    
    import threading

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    #### Global Var ####
    IP = ""
    PORT = ""
    Range = b""
    Gain = b""
    TVG = b""
    Pulse_Width = b""
    Data_List = []
    Save_Data = []
    a_pipe,b_pipe = Pipe()
    ZeroData = np.array([])
    lock = threading.Lock()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    ###Mp
    que_recv = Queue()
    que_send = Queue()
    Data_que = Queue()
    Save_que = Queue()
    Progress_que = Queue()
    Read_que = Queue()

    freeze_support() # EXE File Error REMOVE
    p1 = Process(target=Socket_Connect,args=(que_recv,Data_que,a_pipe),daemon=True)
    p2 = Process(target=Socket_Send,args=(que_send,),daemon=True)
    p3 = Process(target=Save_File,args=(Save_que,Progress_que,),daemon=True)
    p4 = Process(target=Read_File,args=(Read_que,Data_que,),daemon=True)
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    ###EXE
    app = QApplication(sys.argv)
    app.setStyleSheet("QTextEdit {color:white}")
    myWindow = WindowClass()
    myWindow.show()
    app_return = app.exec_()

    Save_que.put(Save_Data)

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    WindowClass._Worker.terminate()
    sys.exit(app_return)
