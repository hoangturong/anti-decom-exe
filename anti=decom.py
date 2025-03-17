import sys
import os
import types
import marshal
import dis
import opcode
import random
import struct
import time
import ctypes
from ctypes import c_int, c_void_p

# Tắt debug và trace ngay lập tức
sys.settrace(None)
sys.setprofile(None)


def hide_console():
    if os.name == 'nt':  # Chỉ áp dụng trên Windows
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
# Phát hiện môi trường bất thường
def detect_advanced_environment():
    start_time = time.time()
    for _ in range(1000000):
        pass
    if time.time() - start_time > 0.5:
        sys.exit(1)

    suspicious_modules = ["uncompyle6", "decompyle3", "pycdc", "pydoc"]
    for mod in suspicious_modules:
        if mod in sys.modules:
            sys.exit(1)

    try:
        with open("/proc/self/status", "r") as f:
            if "TracerPid: 0" not in f.read():
                sys.exit(1)
    except:
        pass

    try:
        with open(sys.argv[0], "rb") as f:
            content = f.read()
        if b"uncompyle" in content.lower() or b"decompyle" in content.lower():
            sys.exit(1)
    except:
        pass

# Tự sửa đổi bytecode
def self_mutate_bytecode():
    try:
        code = compile("pass", "<string>", "exec")
        code_bytes = bytearray(code.co_code)
        for i in range(len(code_bytes)):
            if random.random() > 0.6:
                code_bytes[i] = (code_bytes[i] ^ random.randint(1, 255)) % 256
        marshal.loads(bytes(code_bytes))
    except:
        pass

# Làm rối stack
def stack_corruption():
    for _ in range(random.randint(50, 200)):
        try:
            sys._getframe(random.randint(0, 50))
        except:
            pass

# Gây nhiễu bộ nhớ
def memory_noise():
    try:
        dummy_buffer = ctypes.create_string_buffer(1024 * 1024)
        for i in range(1024 * 1024):
            dummy_buffer[i] = random.randint(0, 255)
        if sys.getallocatedblocks() > 1000000:
            sys.exit(1)
    except:
        pass

# Tích hợp các cơ chế chống dịch ngược
def apply_anti_reverse():
    try:
        hide_console()
        detect_advanced_environment()
        self_mutate_bytecode()
        stack_corruption()
        memory_noise()
    except Exception:
        sys.exit(1)
        
        
#file chính thì thêm: import anti_reverse
# và Gọi hàm áp dụng các cơ chế chống dịch ngược
#anti_reverse.apply_anti_reverse()
