from abc import ABC
from enum import IntEnum


class CommandType(IntEnum):
    CALIBRATE = 0x1
    TRANSLATE = 0x2
    ROTATE = 0x3


class StickId(IntEnum):
    ONE = 0x0,
    TWO = 0x1,
    THREE = 0x2,
    FOUR = 0x3


class BaseCommand(ABC):

    def __init__(self, type: CommandType, stick: StickId, data: int):
        self.type = type
        self.stick = stick
        self.data = data

        if data < 0 or data > 255:
            raise ValueError("Invalid data value", data)

    def serialize(self) -> bytes:
        # 0xFF is used as the start byte
        self.data = min(254, self.data)
        return 0xFF.to_bytes(1, byteorder='big') + \
            self.type.value.to_bytes(1, byteorder='big') + \
            self.stick.value.to_bytes(1, byteorder='big') + \
            self.data.to_bytes(1, byteorder='big')

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type}, stick={self.stick}, data={hex(self.data)})"
