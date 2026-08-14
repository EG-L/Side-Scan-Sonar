# -*- coding: utf-8 -*-
"""
test_sss_mock_sonar.py
-----------------------
실제 소나 하드웨어 없이 SSS_v1.4.4.py 화면에 이미지가 그려지는지 확인하기 위한
'가짜 소나 하드웨어' 역할의 테스트 클라이언트.

SSS_v1.4.4.py는 CONNECT 버튼을 누르면 지정한 IP:PORT로 TCP 서버를 열고
하드웨어의 접속을 기다립니다 (Worker.run 참고). 그리고 수신한 패킷에서
앞쪽 84개 uint16(=168byte)을 헤더로 버리고 나머지를 한 '핑(ping)'의
세기값(uint16 배열)으로 취급해 워터폴 이미지를 그립니다.
(SSS_v1.4.4.py의 Socket_Connect / Worker2 참고)

이 스크립트는 그 반대편, 즉 하드웨어인 척 접속해서
[더미 헤더 84 x uint16] + [세기값 N x uint16] 형태의 패킷을 주기적으로
전송합니다. 화면에는 사인파 + 이동하는 타겟 형태의 무늬가 흘러가며
그려지는 것을 확인할 수 있습니다.

실제 하드웨어와 동일하게, 접속만 해서는 데이터를 보내지 않는다. GUI에서
System Setting에 Range/Gain을 입력하고 Scanning Control의 Start 버튼을 눌러야
그때부터 스트리밍을 시작하고(Stop을 누르면 다시 멈춤), Range 값으로 핑
길이(=이미지 가로폭)를, Gain 값으로 신호 세기(밝기)를 실시간으로 반영한다.

사용법:
    1) SSS_v1.4.4.py 실행 -> HW IP/PORT를 127.0.0.1 / 9090 (기본값) 로 두고
       CONNECT 버튼 클릭 (콘솔에 "NetWork Connected" 로그가 뜨는지 확인)
    2) 이 스크립트를 실행: python test_sss_mock_sonar.py
       -> 접속은 되지만 아직 데이터는 안 보냄 ("Start 대기 중" 로그 확인)
    3) GUI에서 System Setting에 Range/Gain을 입력하고 Scanning Control의
       Start 버튼 클릭 -> 그때부터 하단 Main 워터폴(label_15)과 상단 Signal
       (A-Scope) 그래프에 데이터가 흐르기 시작함
       * Filter 탭의 Color Set 을 Color/Gray 로 바꿔가며 확인 가능
    4) Stop 버튼을 누르면 이 스크립트도 전송을 멈춤 (다시 Start 하면 재개)
"""

import argparse
import socket
import struct
import threading
import time

import numpy as np

HEADER_WORDS = 84   # SSS_v1.4.4.py 가 np.frombuffer(data,"H")[84:] 로 잘라내는 헤더 길이
DEFAULT_DATA_LEN = 500  # Range 제어 패킷을 받기 전까지 사용할 기본 핑 길이

# SSS_v1.4.4.py 가 que_send 로 보내는 제어 패킷 포맷 (Scanning_Start 참고):
#   ZZZZ(4) + packet_len(4) + msg_id(4) + value1(4) + value2(4) = 20byte, 리틀엔디안
CTRL_MAGIC = b"ZZZZ"
CTRL_FMT = "<4siiii"
CTRL_LEN = struct.calcsize(CTRL_FMT)
MSG_START = 2   # Scanning Start
MSG_STOP = 3    # Scanning Stop / NetWork Disconnect
MSG_RANGE = 4   # Range[m] 값
MSG_GAIN = 5    # Gain 값
MSG_TVG = 6     # TVG 콤보박스 인덱스
MSG_PULSE = 7   # Pulse Width 콤보박스 인덱스


DEFAULT_GAIN = 50  # Gain 제어 패킷을 받기 전까지 쓸 기본값 (gain_factor 1.0이 되도록)


class HwState:
    """드레인 스레드와 송신 루프가 공유하는 상태.

    Range -> 핑 길이, Gain -> 신호 세기, Start/Stop -> 전송 여부 동기화용.
    """

    def __init__(self, initial_length: int):
        self.lock = threading.Lock()
        self.length = initial_length
        self.gain = DEFAULT_GAIN
        self.streaming = False  # Start를 눌러야 True, Stop/Disconnect 시 False


def make_header() -> bytes:
    """헤더 내용은 GUI에서 그냥 버려지므로(값 미사용) 0으로 채운다."""
    return np.zeros(HEADER_WORDS, dtype="<u2").tobytes()


def gain_factor(gain: int) -> float:
    """GUI의 Gain 입력값(임의의 정수)을 신호 세기 배율로 변환한다.

    Gain=50 -> 1.0배(기준), Gain=0 -> 0.5배(어두움), Gain=100 -> 1.5배(밝음)
    처럼 대략적인 선형 매핑. 실제 하드웨어의 정확한 스케일은 아니지만,
    Gain을 올리고 내렸을 때 화면 밝기가 눈에 띄게 바뀌는 걸 보기엔 충분하다.
    """
    factor = 0.5 + (gain / 100.0)
    return max(0.2, min(3.0, factor))


def make_ping(step: int, length: int, gain: int) -> bytes:
    """가짜 소나 세기값 한 줄을 생성한다.

    사인파 형태의 반사 신호 + 이동하는 '타겟' 블롭 + 노이즈를 섞고,
    Gain 값에 비례해 전체 세기를 스케일링해서 화면 밝기가 Gain을
    따라가도록 만든다.
    """
    x = np.arange(length)
    factor = gain_factor(gain)

    # 거리에 따라 감쇠하는 배경 반사 신호
    base = 60 * np.exp(-x / (length * 0.6)) * (0.5 + 0.5 * np.sin(x / 15.0))

    # 시간에 따라 좌우로 오가며 이동하는 '타겟' 블롭 (반가운 하이라이트)
    target_pos = length * (0.5 + 0.4 * np.sin(step / 40.0))
    target = 150 * np.exp(-((x - target_pos) ** 2) / (2 * (length * 0.02) ** 2))

    noise = np.random.randint(0, 15, size=length)

    data = np.clip((80 + base + target + noise) * factor, 0, 255).astype("<u2")
    return data.tobytes()


def drain_incoming(sock: socket.socket, state: "HwState", stop_event: threading.Event) -> None:
    """GUI가 Scanning Start 시 보내는 Range/Gain/TVG/제어 패킷을 읽어서
    처리한다. 특히 Range 값을 받으면 핑 길이를 GUI의 Data_Length
    (arange(-Range, Range, 0.02) -> Range*100개) 와 맞춰서, 위쪽 Signal
    그래프(A-Scope)의 x/y 배열 길이가 일치하도록 만든다."""
    sock.settimeout(0.5)
    buf = bytearray()
    while not stop_event.is_set():
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            buf.extend(chunk)
        except socket.timeout:
            continue
        except OSError:
            break

        while len(buf) >= CTRL_LEN:
            if bytes(buf[:4]) != CTRL_MAGIC:
                # 동기화가 어긋났으면 한 바이트씩 버려서 다시 맞춘다.
                del buf[0]
                continue
            packet, buf[:] = bytes(buf[:CTRL_LEN]), buf[CTRL_LEN:]
            _, _pkt_len, msg_id, val1, _val2 = struct.unpack(CTRL_FMT, packet)

            if msg_id == MSG_RANGE:
                with state.lock:
                    state.length = max(val1, 1) * 100
                print(f"[ctrl] Range={val1}m 수신 -> 핑 길이를 {state.length}개로 맞춤")
            elif msg_id == MSG_START:
                with state.lock:
                    state.streaming = True
                print("[ctrl] Scanning Start 수신 -> 데이터 전송 시작")
            elif msg_id == MSG_STOP:
                with state.lock:
                    state.streaming = False
                print("[ctrl] Scanning Stop / Disconnect 수신 -> 데이터 전송 중지")
            elif msg_id == MSG_GAIN:
                with state.lock:
                    state.gain = val1
                print(f"[ctrl] Gain={val1} 수신 -> 신호 세기 배율 {gain_factor(val1):.2f}배로 반영")
            elif msg_id == MSG_TVG:
                print(f"[ctrl] TVG step={val1} 수신")
            elif msg_id == MSG_PULSE:
                print(f"[ctrl] Pulse Width step={val1} 수신")


def main() -> None:
    parser = argparse.ArgumentParser(description="SSS_v1.4.4.py 테스트용 가짜 소나 클라이언트")
    parser.add_argument("--host", default="127.0.0.1", help="SSS GUI의 HW IP (기본값: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=9090, help="SSS GUI의 HW PORT (기본값: 9090)")
    parser.add_argument("--length", type=int, default=DEFAULT_DATA_LEN,
                         help="Range 제어 패킷을 받기 전까지 사용할 초기 핑 길이")
    parser.add_argument("--interval", type=float, default=0.1, help="핑 전송 간격(초)")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    print(f"[connect] SSS GUI 서버 {args.host}:{args.port} 접속 시도 중...")
    sock.connect((args.host, args.port))
    print("[connect] 접속 완료. GUI에서 'NetWork Connected' 로그를 확인하세요.")
    print("[stream] 아직 대기 중 -> GUI에서 Range/Gain 입력 후 Start를 눌러야 전송을 시작함 (Ctrl+C로 종료)")

    state = HwState(args.length)
    stop_event = threading.Event()
    drain_thread = threading.Thread(target=drain_incoming, args=(sock, state, stop_event), daemon=True)
    drain_thread.start()

    step = 0
    was_streaming = False
    try:
        while True:
            with state.lock:
                length, gain, streaming = state.length, state.gain, state.streaming

            if streaming:
                if not was_streaming:
                    print("[stream] 전송 시작")
                packet = make_header() + make_ping(step, length, gain)
                sock.sendall(packet)
                step += 1
                time.sleep(args.interval)
            else:
                if was_streaming:
                    print("[stream] 전송 중지 (Start 대기)")
                time.sleep(0.1)
            was_streaming = streaming
    except KeyboardInterrupt:
        print("\n[stop] 사용자에 의해 중단됨")
    except (ConnectionResetError, BrokenPipeError):
        print("[stop] GUI 쪽에서 연결을 끊었습니다.")
    finally:
        stop_event.set()
        sock.close()


if __name__ == "__main__":
    main()
