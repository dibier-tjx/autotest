import time
import ctypes
import logging
from snap7.client import Client
from snap7.types import Areas, WordLen

logging.basicConfig(level = logging.ERROR, format = '%(asctime)s "%(pathname)s" line %(lineno)s [%(message)s]"')
_logger = logging.getLogger(__name__)

class S7Client:

    _ip: str
    _port: int
    _rack: int
    _slot: int
    _client: Client

    def __init__(self, ip: str = '127.0.0.1', port: int = 102, rack: int = 0, slot: int = 0):
        self._ip = ip
        self._port = port
        self._rack = rack
        self._slot = slot
        self._client = Client()
        
    def _connected_(self) -> bool:
        if not self._client.get_connected():
            self._client.connect(self._ip, self._rack, self._slot, self._port)
        return self._client.get_connected()
        
    def _do_(self, func, retry: int = 3, s: float = 0.05) -> bool:
        while retry > 0:
            if func():
                return True
            time.sleep(s)
            retry -= 1
        return False

    def _read_s7_(self, db_number: int, start: int, size: int, word_len: WordLen, type: ctypes, ms: int = 5000) -> list:
        try:
            buf = (type * size)()
            def func() -> bool:
                return self._connected_() and self._client.as_read_area(Areas.DB, db_number, start, size, word_len, buf) == 0 and self._client.wait_as_completion(ms) == 0
            if self._do_(func):
                res = [None] * size
                for i in range(0, size):
                    res[i] = buf[i]
                return res
        except:
            _logger.error(f'read error: db_number={db_number}, start={start}, size={size}, word_len={word_len.name}, type={type.__name__}')
        return None
        
    def _write_s7_(self, db_number: int, start: int, data: list, word_len: WordLen, amount: int, ms: int = 5000) -> bool:
        try:
            size = len(data)
            buf = (ctypes.c_uint8 * (size * amount))()
            for i in range(0, size):
                for j in range(i, i + amount):
                    if word_len == WordLen.Real:
                        value = ctypes.pointer(ctypes.c_uint32(0))
                        ctypes.memmove(value, ctypes.pointer(ctypes.c_float(data[i])), amount)
                    elif word_len == WordLen.Word:
                        value = ctypes.pointer(ctypes.c_uint16(0))
                        ctypes.memmove(value, ctypes.pointer(ctypes.c_uint16(data[i])), amount)
                    else:
                        _logger.error(f'[word_len={word_len.name}] not support')
                        return False
                    buf[i * (amount - 1) + j] = (value.contents.value >> ((j - i) * 8)) & 0xff
            def func() -> bool:
                return self._connected_() and self._client.as_write_area(Areas.DB, db_number, start, size, word_len, buf) == 0 and self._client.wait_as_completion(ms) == 0
            return self._do_(func)
        except:
            _logger.error(f'write error: db_number={db_number}, start={start}, data={data}, word_len={word_len.name}, amount={amount}')
        return False
    
    def read_u16(self, start: int, size: int = 1, db_number: int = 11) -> list:
        return self._read_s7_(db_number, start, size, WordLen.Word, ctypes.c_uint16)

    def read_f32(self, start: int, size: int = 1, db_number: int = 11) -> list:
        return self._read_s7_(db_number, start, size, WordLen.Real, ctypes.c_float)

    def write_u16(self, start: int, data: list, db_number: int = 11) -> bool:
        return self._write_s7_(db_number, start, data, WordLen.Word, 2)
        
    def write_f32(self, start: int, data: list, db_number: int = 11) -> bool:
        return self._write_s7_(db_number, start, data, WordLen.Real, 4)

if __name__ == "__main__":
    cli = S7Client()

    # single
    cli.write_u16(13, [10086])
    cli.write_f32(14, [10086.1111])
    print(f"read[13] = {cli.read_u16(13)}")
    print(f"read[14] = {cli.read_f32(14)}")

    # multi
    cli.write_u16(10, [666, 777, 888])
    cli.write_f32(20, [123.777, 456.888])
    print(f"read[10,3] = {cli.read_u16(10, 3)}")
    print(f"read[20,2] = {cli.read_f32(20, 2)}")