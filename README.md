# Side-Scan-Sonar

![201009019-3b51ee9a-1605-40ef-adcb-b138cc6661f7](https://user-images.githubusercontent.com/81463782/215061265-b05152d7-6714-456c-89a1-3c713ab80f0c.gif)

Side Scan Sonar(측면주사음탐기) 하드웨어와 TCP 소켓으로 통신하며, 수신한 소나 신호를
실시간 워터폴(Waterfall) 이미지와 A-Scope 그래프로 시각화하는 PySide2 기반 GUI 프로그램입니다.

## 주요 기능

- 소나 하드웨어와 TCP 소켓 연결 (`CONNECT` 버튼 → 지정한 IP:PORT로 서버 오픈, 하드웨어 접속 대기)
- 수신 패킷 파싱 후 실시간 워터폴 이미지 및 Signal(A-Scope) 그래프 표시
- Range / Gain 값에 따른 핑(ping) 길이 및 신호 세기 실시간 반영
- Color / Gray 등 컬러맵 전환 (Filter 탭 > Color Set)
- 수신 데이터를 TDMS 포맷 파일로 저장

## 파일 구성

| 파일 | 설명 |
|---|---|
| `SSS_v1.4.4.py` | 메인 GUI 애플리케이션 (소켓 통신, 데이터 파싱, 시각화, TDMS 저장) |
| `SSSKW.py` | Qt Designer(`SSSKW1.ui`)로부터 생성된 UI 폼 |
| `AL_Conn.py` | 소나 통신 프로토콜(패킷 구조) 실험용 스크립트 |
| `test_sss_mock_sonar.py` | 실제 하드웨어 없이 GUI 동작을 확인하기 위한 가짜 소나 하드웨어(mock) 테스트 클라이언트 |
| `requirements.txt` | 실행에 필요한 파이썬 패키지 목록 |

## 설치

Python 3.x 환경에서 아래 명령으로 의존 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python SSS_v1.4.4.py
```

GUI에서 HW IP/PORT를 입력하고 `CONNECT` 버튼을 누르면 해당 주소로 TCP 서버가 열리며
하드웨어의 접속을 기다립니다.

## 하드웨어 없이 테스트하기

실제 소나 장비가 없어도 `test_sss_mock_sonar.py`로 화면 동작을 확인할 수 있습니다.

1. `SSS_v1.4.4.py` 실행 후 HW IP/PORT를 기본값(`127.0.0.1` / `9090`)으로 두고 `CONNECT` 클릭
   (콘솔에 `NetWork Connected` 로그 확인)
2. 아래 명령으로 mock 클라이언트 실행

   ```bash
   python test_sss_mock_sonar.py
   ```

3. GUI의 System Setting에서 Range/Gain을 입력하고 Scanning Control의 `Start` 버튼 클릭
   → 하단 Main 워터폴과 상단 Signal(A-Scope) 그래프에 데이터가 흐르기 시작
   (Filter 탭의 Color Set을 Color/Gray로 바꿔가며 확인 가능)
4. `Stop` 버튼을 누르면 전송이 중단되고, 다시 `Start`를 누르면 재개됩니다.

## 데이터 저장 포맷

- **저장 파일 포맷**: TDMS (National Instruments의 Technical Data Management Streaming 포맷, 확장자 `.tdms`)
- **사용 라이브러리**: [`nptdms`](https://pypi.org/project/npTDMS/) — 파이썬에서 TDMS 파일을 읽고 쓰기 위한 라이브러리
