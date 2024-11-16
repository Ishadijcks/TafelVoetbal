from communication.commands.commands import BaseCommand, StickId, CommandType


class CalibrateCommand(BaseCommand):
    def __init__(self, stick: StickId):
        super().__init__(CommandType.CALIBRATE, stick, 0x00)
