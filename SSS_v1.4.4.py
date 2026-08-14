from PySide2.QtWidgets import QMainWindow, QApplication,QFileDialog,QStyle
from PySide2.QtCore import QThread,Signal,Slot,QTimer,QEvent
from PySide2.QtGui import QPixmap,Qt

from SSSKW import Ui_MainWindow
import socket
from nptdms import TdmsWriter, ChannelObject,TdmsFile
import numpy as np
import time
from queue import Empty

def _run_ignoring_sigint(target, args):
    """멀티프로세싱 워커 프로세스 진입점 래퍼.

    Windows 콘솔에서 Ctrl+C(SIGINT)는 부모+자식 프로세스 전체 그룹에 함께 전달된다.
    이걸 그냥 두면 워커 프로세스들이 각자 KeyboardInterrupt로 죽으면서 트레이스백만
    잔뜩 찍고, 정작 메인 GUI는 멀쩡히 떠 있는 상태가 된다. 그래서 자식 프로세스는
    SIGINT를 무시하고, 종료는 메인 프로세스가 일괄적으로 처리하도록 한다.
    """
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    target(*args)

def Socket_Connect(que,Dataque,pipe):
    client_Data = ""
    while True:
        try:
            Data = que.get(timeout=0.1)
        except Empty:
            continue
        if type(Data) == socket.socket:
            client_Data = Data
            try:
                while True:
                    Send_Data = client_Data.recv(65536)
                    if not Send_Data:
                        # 상대(하드웨어)가 연결을 정상 종료함 -> 루프 종료
                        break
                    if Send_Data == b'ZZZZ\x14\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00':
                        continue
                    try:
                        pipe.send(np.frombuffer(Send_Data,dtype="H")[84:])
                    except Exception as parse_err:
                        # 패킷이 쪼개지거나 손상된 경우 이번 프레임만 버리고 수신은 계속
                        print("Malformed sonar packet skipped:", parse_err)
                        continue
            except Exception as e:
                print(e)
            finally:
                pipe.close()
                client_Data.close()

def Socket_Send(que):
    client_Data = ""
    while True:
        try:
            Data = que.get(timeout=0.1)
        except Empty:
            continue

        if type(Data) == socket.socket:
            client_Data = Data
            continue

        if type(client_Data) != socket.socket:
            # 아직 연결된 적이 없는 상태에서 들어온 명령(Close 포함)은 조용히 버림
            # ('str' object has no attribute 'send'/'close' 오류 방지)
            continue

        try:
            if Data == "Close":
                client_Data.close()
            else:
                client_Data.send(Data)
        except Exception as e:
            print(e)
            try:
                client_Data.close()
            except Exception:
                pass

FLUSH_EVERY_N_FRAMES = 10  # 몇 프레임마다 한 번씩 강제로 디스크에 내보낼지

def Save_File(que,proque):
    """스캔 중 들어오는 프레임을 바로바로 디스크에 스트리밍으로 기록한다.

    예전엔 "Start"~"Stop" 사이에 캡처한 프레임 전체를 리스트(Save_Data)에
    다 쌓아뒀다가 Stop 시점에 한 번에 저장했음 -> 세션이 길어질수록 메모리가
    끝없이 늘고, 리스트 맨 앞에 계속 insert(0,...)하는 비용도 O(n)이라 갈수록
    느려지는 문제가 있었음. 대신 "Start" 신호를 받으면 그 즉시 파일을 열어두고,
    프레임이 하나씩 들어올 때마다 바로 write_segment로 기록한 뒤 "Stop"에서
    파일을 닫는다. 메모리엔 항상 처리 중인 프레임 하나만 남는다.
    """
    from time import ctime
    import re

    tdms_writer = None
    frame_idx = 0

    while True:
        try:
            msg = que.get(timeout=0.1)
        except Empty:
            continue

        # msg가 numpy 배열(프레임)일 수 있어서, 문자열 여부를 먼저 확인한 뒤에
        # "Start"/"Stop"과 비교해야 한다. isinstance 체크 없이 바로 배열을 문자열과
        # == 비교하면 원소별로 비교돼서 bool 배열이 나오고, if문이 그 배열의
        # 참/거짓을 판단 못 해서 "ValueError: truth value of an array ... is
        # ambiguous"로 이 프로세스 자체가 죽어버린다 (실제로 이 버그 때문에
        # 스캔 중 첫 프레임이 들어오자마자 Save_File이 크래시하고 있었음).
        if isinstance(msg, str) and msg == "Start":
            if tdms_writer is not None:
                # 비정상적으로 이전 파일이 안 닫힌 채 남아있었다면 먼저 정리
                # (예: Stop 없이 Start를 다시 누른 경우) -> 이전 파일을 완성된
                # 상태로 마무리해서 데이터 유실을 줄인다.
                try:
                    tdms_writer.close()
                except Exception as e:
                    print("[Save_File] 이전 파일 정리 실패:", repr(e))

            time_D = ctime()
            time_D = re.sub(" |:","_",time_D)
            path = './KW_CSV_SSSData/%s_DataKW.tdms'%time_D
            tdms_writer = TdmsWriter(path)
            tdms_writer.open()
            frame_idx = 0

        elif isinstance(msg, str) and msg == "Stop":
            if tdms_writer is not None:
                try:
                    tdms_writer.close()
                except Exception as e:
                    print("[Save_File] 파일 닫기 실패:", repr(e))
                tdms_writer = None
            proque.put("Done")

        elif tdms_writer is not None:
            # msg = 프레임 하나 (numpy 배열)
            write_ok = False
            try:
                channel = ChannelObject('Sonar Data','Data %s'%frame_idx,msg)
                tdms_writer.write_segment([channel])
                frame_idx += 1
                write_ok = True
            except Exception as e:
                print("[Save_File] 기록 실패:", repr(e))

            # 쓰기 자체가 실패했으면 flush를 시도할 이유가 없음 -> 별개로 분리해서,
            # flush 실패가 "기록 실패"로 잘못 찍히지 않게 한다.
            if write_ok and frame_idx % FLUSH_EVERY_N_FRAMES == 0:
                # TdmsWriter는 flush()를 공개 API로 제공하지 않아서 내부 파일
                # 객체에 직접 접근함. 매 프레임마다 하면 디스크 I/O 호출이 너무
                # 잦아지니, N프레임마다 한 번씩만 내보내서 탐색기에서 파일
                # 크기가 주기적으로 늘어나는 걸 볼 수 있게 한다.
                try:
                    tdms_writer._file.flush()
                except AttributeError:
                    pass
                except Exception as e:
                    print("[Save_File] flush 실패:", repr(e))

def Read_File(que,Data_Que):
    import time
    Data = 0
    Range = 0
    Step = 0.1
    while True:
        try:
            Data_Read = que.get(timeout=0.1)
        except Empty:
            continue

        if type(Data_Read) == list:
            Data = Data_Read[::-1]
            Range = 0
            print("[Read_File] 파일 데이터 수신:", len(Data), "프레임")
        elif type(Data_Read) == float:
            pass
        elif type(Data_Read) == int:
            Range = Data_Read
        elif Data_Read == 'Readit':
            print("[Read_File] 재생 시작: Range=%s, 전체 프레임=%s" % (Range, len(Data) if Data != 0 else 0))
            while True:
                try:
                    if que.qsize() != 0 :
                        Data_ = que.get()
                        if Data_ == 'Stop':
                            print("[Read_File] Stop 수신, 재생 중단")
                            break
                        elif type(Data_) == float:
                            Step = Data_
                        elif type(Data_) == int:
                            Range = Data_
                    if len(Data) == Range:
                        print("[Read_File] 끝까지 재생 완료")
                        break

                    Data_Que.put(Data[Range])
                    time.sleep(Step)
                    Range+=1
                except Exception as e:
                    print("[Read_File]", repr(e))
                    break

class Worker(QThread):
    Conn_S = Signal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.client = ""
        self.parent = parent
        self._stop_flag = False

    def run(self):
        global IP, PORT,sock
        self._stop_flag = False
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((IP,int(PORT)))
        sock.listen(1)
        # accept()가 무한정 블로킹되지 않도록 타임아웃을 주고 stop 플래그를 주기적으로 확인한다.
        # (다른 스레드에서 이 소켓을 close() 해서 블로킹을 깨우면 Windows에서
        #  "WinError 10038: 소켓 이외의 개체에 작업을 시도했습니다" 가 발생할 수 있음)
        sock.settimeout(0.5)

        try:
            while not self._stop_flag:
                try:
                    self.client, self.addr = sock.accept()
                except socket.timeout:
                    continue
                self.parent.Check_NetworkConnection = True
                self.Conn_S.emit("NetWork Connected : {}".format(self.addr))
                que_recv.put(self.client)
                que_send.put(self.client)
        except Exception as e:
            pass
        finally:
            sock.close()

    def stop(self):
        self._stop_flag = True
        if type(self.client) != str:
            try:
                self.client.close()
            except OSError:
                pass

class Worker2(QThread):
    Data_Send = Signal(list)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.cnt = 0
        self.Range_Speed = 0
        self.Range_Copy = 0

    def run(self):
        global Data_que,Data_List,lock,ZeroData,Read_que,b_pipe,Save_que

        img_ = None
        while True:
            if self.parent.Data_Read_Stop == False:
                try:
                    if self.parent.Read_File:
                        # File Mode 재생 데이터는 Read_File 프로세스가 Data_que 로 보냄.
                        # (b_pipe는 실시간 네트워크 데이터 전용 경로라 File Mode에서는
                        #  아무 데이터도 오지 않아 재생 버튼이 동작하지 않던 원인)
                        try:
                            Data = Data_que.get(timeout=0.05)
                        except Empty:
                            continue
                    else:
                        # b_pipe.recv()는 원래 타임아웃 없이 무한 블로킹이라,
                        # 앱을 켠 직후(아직 Read_File=False) 네트워크에 연결한 적이
                        # 없으면 여기서 영원히 멈춰버린다. 그 뒤 File Mode로 전환해도
                        # 이미 이 호출에 갇혀 있어서 Read_File이 True로 바뀐 걸
                        # 다시 확인할 기회가 없었음(재생 버튼이 안 먹히던 원인).
                        # poll()로 짧게 확인해서 루프가 주기적으로 위 분기를
                        # 다시 타도록 한다.
                        if not b_pipe.poll(0.05):
                            continue
                        Data = b_pipe.recv()
                    if type(Data) == str:
                        Data_List.clear()
                    lock.acquire()
                    # ==(정확히 같을 때만) 대신 >=로: 레이스로 인해 높이를 한 번에
                    # 건너뛰면(예: moving_Slider가 한꺼번에 여러 프레임을 채워 넣는 경우)
                    # ==만으로는 다시는 안 맞아서 Data_List가 무한정 커질 수 있었음.
                    while len(Data_List) >= self.parent.widget_2.height() and len(Data_List) > 0:
                        Data_List.pop()
                    lock.release()

                    if len(Data) == 0:
                        Data = ZeroData
                
                    self.Data_Send.emit(Data)

                    if self.parent.Read_File == False:
                        # 저장은 원본(raw) 그대로 -> File Mode로 재생할 때도 Signal(A-Scope)
                        # 그래프가 실시간 모드와 같은 진짜 신호 크기를 보여줄 수 있게 함.
                        # (예전엔 여기서 0~255로 클리핑한 값을 저장해서, 재생 시 A-Scope가
                        #  실시간보다 훨씬 얇고 밋밋하게 보였음 - 저장 시점에 신호가 이미 잘려서
                        #  저장된 파일이었음)
                        # 예전엔 Save_Data 리스트에 계속 쌓았다가 Stop 시점에 한 번에
                        # 저장했음(세션이 길어질수록 메모리 무제한 증가 + insert(0,...)가
                        # 갈수록 느려지는 문제). Save_File이 Start 때 이미 파일을 열어두고
                        # 있으므로 프레임을 바로바로 스트리밍으로 흘려보낸다.
                        Save_que.put(np.array(Data))

                    # 이미지(워터폴)는 8비트 컬러맵이 필요하므로 여기서만 0~255로 클리핑.
                    # Live/File 모드 둘 다 동일하게 적용해서 이미지 표시는 항상 일관되게 만든다.
                    Image_Data = np.where(np.array(Data)>255,255,np.array(Data).astype(np.uint8))

                    lock.acquire()
                    Data_List.insert(0,Image_Data)
                    lock.release()

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
                            # 슬라이더를 처음(0)으로 되돌려야 재생 버튼을 다시 눌렀을 때
                            # Read_Save_Data의 "maximum() != value()" 조건이 만족되어 재생됨
                            self.parent.horizontalSlider.setValue(0)
                            # 수동 Stop과 달리 여기선 Data_Read_Stop을 안 건드려서,
                            # 끝까지 재생된 뒤에도 Worker2가 계속 깨어있는 채로
                            # Data_que를 계속 확인(Empty->continue)했음. continue도
                            # finally 블록을 타므로, 그때마다 직전에 계산해둔 오래된
                            # img_로 label_15를 계속 다시 그려서 Color/Gray를 바꿔도
                            # 그 결과가 곧바로 옛날 이미지로 덮여버렸었다(끝까지
                            # 재생됐을 때만 재현되던 원인). 수동 Stop과 동일하게
                            # 정지 상태로 만들어서 더 이상 재그리지 않게 한다.
                            self.parent.Data_Read_Stop = True

                    if len(Data_List)!=0:

                        if self.parent.comboBox_3.currentText() == 'Color':
                            try:
                                img = applyColorMap(np.array(Data_List.copy()),COLORMAP_OCEAN)
                                img = resize(img,dsize=(self.parent.widget_2.width(),img.shape[0]),interpolation=INTER_AREA)
                                img_ = fromarray(img,'RGB')
                            except Exception as e:
                                lock.acquire()
                                if Data_List:
                                    Data_List.pop(0)
                                lock.release()
                        else:
                            img_ = fromarray(np.require(Data_List,np.int8,'C'),'L')
                except Exception as e:
                    print("[Worker2]", repr(e))
                    continue
                finally:
                    if img_ is not None:
                        qim = ImageQt(img_).copy()
                        self.image = QPixmap.fromImage(qim)
                        self.parent.label_15.setScaledContents(True)
                        self.parent.label_15.setPixmap(self.image)
            else:
                # Data_Read_Stop 상태에서 CPU를 계속 스핀하지 않도록 짧게 대기
                self.msleep(20)

class Worker3(QThread):
    D_Log = Signal(str)
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        global Progress_que,Data_List,lock
        while True:
            try:
                Progress_Data = Progress_que.get(timeout=0.1)
            except Empty:
                continue
            if Progress_Data == "Done":
                lock.acquire()
                try:
                    Data_List.clear()
                    self.D_Log.emit("File Save Done")
                finally:
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
            # 예전엔 콘솔에만 print(e) 하고 조용히 끝나서, 빈 파일이나 형식이
            # 다른 tdms 파일을 열었을 때 사용자는 "재생을 눌러도 아무 반응 없음"
            # 으로만 보였음 -> GUI 로그창에도 원인을 남긴다.
            self.parent.Show_Image.clear()
            # 이전에 성공적으로 불러온 파일의 슬라이더 범위가 그대로 남아있으면
            # 화면엔 옛날 파일 길이가 표시된 채로 새 파일은 비어있는 혼란스러운
            # 상태가 됨 -> 실패 시 슬라이더/카운터도 같이 초기화.
            self.parent.horizontalSlider.setRange(0,0)
            self.parent.horizontalSlider.setValue(0)
            self.parent.label_18.setText("0/0")
            self.Log_Send.emit("파일 읽기 실패: {} (소나 데이터가 없는 파일일 수 있습니다)".format(e))

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

        # 슬라이더 막대(그루브)를 클릭하면 기본 QSlider는 핸들 쪽으로 한 스텝만
        # 움직이는데, 재생바처럼 클릭한 위치로 바로 점프하도록 이벤트를 가로챈다.
        self.horizontalSlider.installEventFilter(self)

        # Color/Gray 전환은 원래 Worker2가 다음 프레임을 처리할 때만 반영됨.
        # 정지 상태(File Mode 일시정지 등)에선 Worker2가 잠들어 있어서 새
        # 프레임이 안 오니까 드롭박스를 바꿔도 화면이 안 바뀌었음 -> 바뀌는
        # 즉시 현재 Data_List로 다시 그리도록 연결.
        self.comboBox_3.currentIndexChanged.connect(lambda _: self._render_waterfall_now())

        # QThread 연동
        self._Worker.Conn_S.connect(self.Data_Log)
        self._Worker2.Data_Send.connect(self.Draw_AScope)
        self._Worker3.D_Log.connect(self.Data_Log)
        self._Worker4.Log_Send.connect(self.Data_Log)
        self._Worker4.AScope_Send.connect(self.Draw_AScope)

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

        # Thread 시작
        # 주의: Worker2.run()이 시작하자마자 self.Data_Read_Stop / self.Read_File
        # 같은 인스턴스 속성을 바로 읽으므로, 그 값들을 전부 설정한 "다음"에
        # 스레드를 시작해야 한다. 예전엔 start()가 이 초기값들보다 먼저 호출돼서,
        # 스레드가 먼저 실행되는 타이밍이 걸리면(레이스 컨디션) 아직 속성이
        # 만들어지기도 전에 접근해서 AttributeError로 죽는 문제가 있었다.
        self._Worker2.start()

    def resizeEvent(self, event):

        global Data_List,lock
        lock.acquire()
        Data_List.clear()
        lock.release()

    def eventFilter(self, obj, event):
        if obj is self.horizontalSlider and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # 핸들/그루브를 구분하려 하지 않고, 클릭 위치로 값을 바로 옮긴 뒤
            # 이벤트는 막지 않고 그대로 Qt 기본 처리로 흘려보낸다.
            # (subControlRect로 핸들 영역을 구분해서 그루브 클릭만 가로채려
            #  했더니 감지가 제대로 안 맞아서 아예 반응이 없었음. 이벤트를
            #  consume하지 않으면 핸들을 눌러 끄는 기존 드래그도 그대로 살아있고,
            #  그루브를 클릭했을 때도 이 코드가 먼저 정확한 위치로 이동시켜준다.)
            value = QStyle.sliderValueFromPosition(
                self.horizontalSlider.minimum(),
                self.horizontalSlider.maximum(),
                event.x(),
                self.horizontalSlider.width())
            self.horizontalSlider.setValue(value)
            self.moving_Slider()
        return super().eventFilter(obj, event)

    def Stop_Save_Data(self):
        global Read_que,lock
        if self.Start_NetWorking == False:
            self.Data_Read_Stop = True
            self.Start_Data = False
            lock.acquire()
            Read_que.put("Stop")
            lock.release()

    def _rebuild_data_list_for_position(self, pos):
        """Show_Image에서 pos(재생 위치)에 해당하는 구간을 Data_List에 즉시 채운다.

        화면을 지웠다가 스트리밍으로 한 프레임씩 다시 채우길 기다리는 대신(그러면
        지워졌다 다시 그려지는 것처럼 보임), 이미 메모리에 있는 데이터로 그 자리에서
        바로 이어그리듯 보여주기 위함. 슬라이더 이동/클릭과 재생 재개(Play) 양쪽에서 씀.
        """
        try:
            height = self.widget_2.height()
            frames = self.Show_Image[::-1]  # Read_File과 동일한 순서(오래된 것 -> 최신)
            window = frames[max(0, pos - height):pos]
            window.reverse()  # Data_List 관례: index 0 = 가장 최근(위쪽)

            # Signal(A-Scope)은 Worker2가 실제로 새 프레임을 처리할 때만
            # (Data_Send.emit) 갱신되는데, 정지 상태에서 슬라이더만 움직이면
            # Worker2는 잠들어 있어서 안 바뀜 -> Main 이미지와 같이 즉시 동기화.
            # 클리핑 전 원본(raw) 값을 써야 실시간/재생 중일 때와 동일하게 보임.
            if window:
                self.Draw_AScope(window[0])

            # 이미지는 8비트(0~255) 컬러맵이 필요함. Save_Data/Show_Image는 Signal
            # 그래프 재현을 위해 원본(raw, 255 초과 가능) 값을 담고 있을 수 있어서,
            # Worker2의 스트리밍 경로와 동일하게 여기서도 클리핑해야 함
            # (안 하면 applyColorMap이 조용히 실패해서 Main 화면이 안 움직였음).
            window = [np.where(np.array(f)>255,255,np.array(f).astype(np.uint8)) for f in window]
            Data_List.clear()
            Data_List.extend(window)
        except Exception:
            Data_List.clear()

    def moving_Slider(self):
        global Read_que,lock,Data_que
        if self.Start_NetWorking == False:
            pos = self.horizontalSlider.value()
            lock.acquire()
            self.label_18.setText("%i/%i"%(pos,len(self.Show_Image)))
            Read_que.put(pos)
            self._rebuild_data_list_for_position(pos)
            lock.release()

            self._render_waterfall_now()

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
        was_connected = self.Check_NetworkConnection
        self.Check_NetworkConnection = False
        Data_List.clear()
        if was_connected:
            # 실제로 접속된 적이 없으면 Socket_Send 쪽 client_Data가 여전히 ""(str)라서
            # send/close를 시도하면 AttributeError만 찍힘 -> 연결됐을 때만 정지 패킷 전송
            que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
            que_send.put("Close")
        self._Worker.stop()
        self.Data_Log("NetWork Disconnected")

    def Scanning_Start(self):
        global Range,Gain,TVG,Pulse_Width,Save_que,ZeroData,Data_List,que_recv
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
                        que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

                        for i in Send_Data:
                            que_send.put(i)

                        que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')

                        # 예전엔 Stop을 누를 때까지 Save_Data 리스트에 다 쌓아뒀다가
                        # 한 번에 저장했음(메모리 무제한 증가 문제). 이제 Start 시점에
                        # 바로 새 파일을 열어서 프레임을 스트리밍으로 기록한다.
                        Save_que.put("Start")

                        self.Data_Log("System Start")
            except Exception as e:
                self.MessageBox.about(self,'Alert','잘못된 값을 입력하셨습니다.')

    def Scanning_Stop(self):
        global Data_List,Save_que
        if self.Start_Data == False:
            if self.Start_NetWorking == True:
                self.Data_Read_Stop = True
                self.Start_NetWorking = False
                que_send.put(b'\x5A\x5A\x5A\x5A\x14\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
                # 이제 프레임을 스트리밍으로 바로 저장하고 있으므로, 큰 리스트를
                # 통째로 넘기는 대신 파일을 닫으라는 신호만 보낸다.
                Save_que.put("Stop")
                self._Worker3.start()

                self.Data_Log("System Stop")

    def FileOpen(self):
        global Data_List,Read_que
        if self.Start_NetWorking == True:
            self.MessageBox.about(self,'Alert','Stop버튼을 먼저 눌러주세요.')
        else:
            QFileName = QFileDialog.getOpenFileName(None,'Open File',"./")[0]
            if not QFileName:
                return  # 파일 선택 취소
            try:
                self.Read_File = True
                if Read_que.qsize() != 0:
                    Read_que.put("Stop")
                    Data_List.clear()
                self.tdms_file = TdmsFile(QFileName)
                self._Worker4.start()
            except Exception as e:
                self.Data_Log("파일 열기 실패: {}".format(e))

    def _render_waterfall_now(self):
        """Data_List 내용을 지금 즉시 label_15에 반영한다.

        Worker2의 렌더링 로직과 사실상 동일하지만, 이건 GUI 스레드(슬라이더 이동 등)에서
        바로 호출되어 Worker2가 다음 프레임을 받을 때까지(File Mode 일시정지 중이면
        영영) 기다리지 않고 화면을 즉시 갱신한다.
        """
        try:
            if len(Data_List) == 0:
                return
            if self.comboBox_3.currentText() == 'Color':
                img = applyColorMap(np.array(Data_List.copy()),COLORMAP_OCEAN)
                img = resize(img,dsize=(self.widget_2.width(),img.shape[0]),interpolation=INTER_AREA)
                img_ = fromarray(img,'RGB')
            else:
                img_ = fromarray(np.require(Data_List,np.int8,'C'),'L')
            qim = ImageQt(img_).copy()
            self.label_15.setScaledContents(True)
            self.label_15.setPixmap(QPixmap.fromImage(qim))
        except Exception as e:
            print("[_render_waterfall_now]", repr(e))

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
        global Data_List,Read_que,lock
        if self.Start_NetWorking == False:
            if len(self.Show_Image) == 0:
                return
            if self.horizontalSlider.maximum() == self.horizontalSlider.value():
                # 끝까지 재생됐거나 슬라이더를 끝으로 옮겨 놓은 상태에서 재생을
                # 누르면 예전엔 아무 반응이 없었음(조건 불일치로 조용히 무시됨).
                # 이 경우엔 처음부터 다시 재생하도록 함.
                self.horizontalSlider.setValue(0)
            self.Data_Read_Stop = False
            self.Start_Data = True
            self.Read_File = True
            # 예전엔 여기서 Data_List.clear()로 화면을 통째로 비우고 스트리밍이
            # 다시 채워주길 기다렸음 -> 정지 후 재생을 누르면 화면이 지워졌다가
            # 다시 그려지는 것처럼 보였음. 대신 현재 위치에 맞는 내용으로 즉시
            # 다시 채워서 끊김 없이 이어그리듯 보이게 한다.
            lock.acquire()
            self._rebuild_data_list_for_position(self.horizontalSlider.value())
            lock.release()
            self._render_waterfall_now()
            self._Worker4.ReadAll()
            Read_que.put(self.horizontalSlider.value())


if __name__ == "__main__":
    import sys
    import signal
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
    p1 = Process(target=_run_ignoring_sigint,args=(Socket_Connect,(que_recv,Data_que,a_pipe)),daemon=True)
    p2 = Process(target=_run_ignoring_sigint,args=(Socket_Send,(que_send,)),daemon=True)
    p3 = Process(target=_run_ignoring_sigint,args=(Save_File,(Save_que,Progress_que,)),daemon=True)
    p4 = Process(target=_run_ignoring_sigint,args=(Read_File,(Read_que,Data_que,)),daemon=True)
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    ###EXE
    app = QApplication(sys.argv)
    app.setStyleSheet("QTextEdit {color:white}")
    myWindow = WindowClass()
    myWindow.show()

    # Ctrl+C(SIGINT)를 눌렀을 때 GUI가 반응하도록 처리.
    # PySide2 이벤트 루프(app.exec_())는 C++ 쪽에서 블로킹되어 있어서
    # 파이썬 인터프리터가 시그널을 확인할 기회 자체가 없다. 짧은 주기로
    # 아무 동작 안 하는 QTimer를 돌려서 인터프리터에 주기적으로 제어권을
    # 돌려주면, SIGINT 핸들러(app.quit())가 실제로 실행될 수 있다.
    signal.signal(signal.SIGINT, lambda signum, frame: app.quit())
    _sigint_pump = QTimer()
    _sigint_pump.timeout.connect(lambda: None)
    _sigint_pump.start(200)

    app_return = app.exec_()

    # 스캔 중에 그냥 창을 닫았다면 Save_File이 파일을 열어둔 채로 남아있을 수
    # 있으므로, 프로세스를 죽이기 전에 정지 신호를 보내서 제대로 닫히게 한다.
    # (스캔 중이 아니었다면 Save_File은 그냥 아무 것도 안 하고 "Done"만 보고함)
    Save_que.put("Stop")
    try:
        Progress_que.get(timeout=2)
    except Empty:
        pass

    # p1~p4는 종료 신호가 없는 while True 루프라 join()만 하면 영원히 멈추지 않는다.
    # daemon=True 프로세스이므로 강제로 terminate 해도 안전하다.
    for p in (p1, p2, p3, p4):
        p.terminate()
    for p in (p1, p2, p3, p4):
        p.join(timeout=2)

    myWindow._Worker.terminate()
    sys.exit(app_return)
