import ctypes
import ctypes.util
import os
import sys

if sys.platform == "win32":
    # 로컬 Windows 테스트용: find_library가 유닉스 관례라 윈도우에선 안 먹으므로
    # Anaconda에 이미 깔려있는 OpenSSL DLL을 직접 지정 (리눅스 배포 시엔 이 분기 안 탐)
    _libcrypto_path = r"C:\Anaconda3\Library\bin\libcrypto-1_1-x64.dll"
else:
    _libcrypto_path = ctypes.util.find_library("crypto")

if not _libcrypto_path:
    raise RuntimeError("libcrypto(OpenSSL)를 찾을 수 없습니다. `ldconfig -p | grep libcrypto`로 확인하세요.")
_lib = ctypes.CDLL(_libcrypto_path)

# 포인터 인자가 있는 함수는 반드시 argtypes를 선언해야 함
# (안 하면 64비트 주소값이 32비트로 잘리거나 OverflowError로 죽음)
_lib.EVP_CIPHER_CTX_new.restype = ctypes.c_void_p
_lib.EVP_CIPHER_CTX_new.argtypes = []

_lib.EVP_CIPHER_CTX_free.restype = None
_lib.EVP_CIPHER_CTX_free.argtypes = [ctypes.c_void_p]

_lib.EVP_aes_256_cbc.restype = ctypes.c_void_p
_lib.EVP_aes_256_cbc.argtypes = []

_lib.EVP_EncryptInit_ex.restype = ctypes.c_int
_lib.EVP_EncryptInit_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]
_lib.EVP_DecryptInit_ex.restype = ctypes.c_int
_lib.EVP_DecryptInit_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p]

_lib.EVP_EncryptUpdate.restype = ctypes.c_int
_lib.EVP_EncryptUpdate.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int]
_lib.EVP_DecryptUpdate.restype = ctypes.c_int
_lib.EVP_DecryptUpdate.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.c_char_p, ctypes.c_int]

_lib.EVP_EncryptFinal_ex.restype = ctypes.c_int
_lib.EVP_EncryptFinal_ex.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]
_lib.EVP_DecryptFinal_ex.restype = ctypes.c_int
_lib.EVP_DecryptFinal_ex.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int)]


def _cipher(key: bytes, iv: bytes, data: bytes, encrypting: bool) -> bytes:
    assert len(key) == 32 and len(iv) == 16
    ctx = _lib.EVP_CIPHER_CTX_new()
    if not ctx:
        raise RuntimeError("EVP_CIPHER_CTX_new 실패")
    try:
        init = _lib.EVP_EncryptInit_ex if encrypting else _lib.EVP_DecryptInit_ex
        update = _lib.EVP_EncryptUpdate if encrypting else _lib.EVP_DecryptUpdate
        final = _lib.EVP_EncryptFinal_ex if encrypting else _lib.EVP_DecryptFinal_ex

        if init(ctx, _lib.EVP_aes_256_cbc(), None, key, iv) != 1:
            raise RuntimeError("암호화 초기화 실패")

        outbuf = ctypes.create_string_buffer(len(data) + 32)
        outlen = ctypes.c_int(0)
        if update(ctx, outbuf, ctypes.byref(outlen), data, len(data)) != 1:
            raise RuntimeError("Update 실패")
        total = outlen.value

        finlen = ctypes.c_int(0)
        # outbuf 중간 지점(offset=total)을 가리키는 포인터.
        # byref(outbuf, total)는 c_char_p argtype과 타입이 안 맞아 ArgumentError가 나서
        # addressof + cast 방식으로 명시적 포인터를 만들어 넘긴다.
        final_ptr = ctypes.cast(ctypes.addressof(outbuf) + total, ctypes.c_char_p)
        # 키/IV가 틀리면 복호화 시 여기서 실패함 (패딩 검증 실패) — 이게 정상
        if final(ctx, final_ptr, ctypes.byref(finlen)) != 1:
            raise RuntimeError("복호화 실패: 키가 틀렸거나 데이터가 손상됨")
        total += finlen.value

        return outbuf.raw[:total]
    finally:
        _lib.EVP_CIPHER_CTX_free(ctx)


def encrypt(key: bytes, plaintext: bytes) -> bytes:
    iv = os.urandom(16)
    return iv + _cipher(key, iv, plaintext, encrypting=True)


def decrypt(key: bytes, blob: bytes) -> bytes:
    iv, ciphertext = blob[:16], blob[16:]
    return _cipher(key, iv, ciphertext, encrypting=False)


if __name__ == "__main__":
    key = os.urandom(32)

    for plaintext in [b"DB_PASSWORD_1234", b"", b"a", b"x" * 100, "한글비밀번호".encode("utf-8")]:
        enc = encrypt(key, plaintext)
        dec = decrypt(key, enc)
        print("enc : {}, dec : {}".format(enc,dec))
        status = "OK" if dec == plaintext else "FAIL"
        print(f"[{status}] plaintext={plaintext!r} -> decrypted={dec!r}")

    # 틀린 키로 복호화 시도 -> 에러가 나야 정상 (조용히 이상한 값 주면 안 됨)
    try:
        wrong_key = os.urandom(32)
        decrypt(wrong_key, encrypt(key, b"secret"))
        print("[FAIL] 틀린 키인데도 에러 없이 통과함 (위험)")
    except RuntimeError as e:
        print(f"[OK] 틀린 키 -> 정상적으로 에러 발생: {e}")
