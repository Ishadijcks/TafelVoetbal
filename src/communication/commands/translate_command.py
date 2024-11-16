from communication.commands.commands import BaseCommand, StickId, CommandType


class TranslateCommand(BaseCommand):
    def __init__(self, stick: StickId, fraction: float):
        if fraction < 0 or fraction > 1:
            raise ValueError(f"Fractions must be between 0 and 1, was '{fraction}'")

        data = int(fraction * ((1 << 16) - 1))
        super().__init__(CommandType.TRANSLATE, stick, data.to_bytes(2, 'big'))
