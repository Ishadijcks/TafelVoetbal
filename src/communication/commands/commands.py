from abc import ABC
from enum import IntEnum


class CommandType(IntEnum):
    CALIBRATE = 0x1
    TRANSLATE = 0x2
    ROTATE = 0x3


class StickId(IntEnum):
    ONE = 0x1,
    TWO = 0x2,
    THREE = 0x3,
    FOUR = 0x4


class BaseCommand(ABC):

    def __init__(self, type: CommandType, stick: StickId, data: bytes):
        self.type = type
        self.stick = stick
        self.data = data

        if len(data) != 2:
            raise ValueError(f"Invalid data length, must be 2 bytes, is '{len(data)}'")

    def serialize(self) -> bytes:
        return self.type.value.to_bytes(1, byteorder='big') + self.stick.value.to_bytes(1, byteorder='big') + self.data

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type}, stick={self.stick}, data={self.data.hex()})"
