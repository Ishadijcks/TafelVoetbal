from communication.commands.calibrate_command import CalibrateCommand
from communication.commands.commands import StickId
from communication.commands.rotate_command import RotateCommand
from communication.commands.translate_command import TranslateCommand


def test_serialize_calibrate():
    command = CalibrateCommand(StickId.ONE)

    serialized = command.serialize()
    assert serialized == bytes([0x01, 0x01, 0x00, 0x00])


def test_serialize_translate_zero():
    command = TranslateCommand(StickId.FOUR, 0.0)

    serialized = command.serialize()
    assert serialized == bytes([0x02, 0x04, 0x00, 0x00])


def test_serialize_translate_one():
    command = TranslateCommand(StickId.FOUR, 1)

    serialized = command.serialize()
    assert serialized == bytes([0x02, 0x04, 0xFF, 0xFF])


def test_serialize_translate_half():
    command = TranslateCommand(StickId.THREE, 0.5)

    serialized = command.serialize()
    assert serialized == bytes([0x02, 0x03, 0x7F, 0xFF])


def test_serialize_rotate_zero():
    command = RotateCommand(StickId.TWO, 0.0)

    serialized = command.serialize()
    assert serialized == bytes([0x03, 0x02, 0x00, 0x00])


def test_serialize_rotate_one():
    command = RotateCommand(StickId.FOUR, 1)

    serialized = command.serialize()
    assert serialized == bytes([0x03, 0x04, 0xFF, 0xFF])


def test_serialize_rotate_half():
    command = RotateCommand(StickId.ONE, 0.5)

    serialized = command.serialize()
    assert serialized == bytes([0x03, 0x01, 0x7F, 0xFF])
