from communication.commands.commands import BaseCommand, StickId
from communication.commands.translate_command import TranslateCommand
from model.game_state import GameState
from strategy.strategy import Strategy


class FollowStrategy(Strategy):
    """
    Tries to place the keeper at the position of the ball
    """

    def __init__(self):
        super().__init__()

    def execute(self, previous_state: GameState, state: GameState, delta: float) -> list[BaseCommand]:
        commands = []
        ball_x, ball_y = state.ball

        # If the ball is not on our half, return to center, otherwise try to follow it
        if ball_x > 0.5:
            commands.append(TranslateCommand(StickId.ONE, 0.5))
        elif ball_x > 0.25:
            # Position between ball and center
            target_position = (0.5 + ball_y) / 2
            commands.append(TranslateCommand(StickId.ONE, target_position))
        else:
            # TODO convert between ball and keeper space
            #  Make global calculations regarding semantical state
            clipped_ball = min(0.66, max(0.33, ball_y)) - 0.33

            target_position = clipped_ball / 0.33
            commands.append(TranslateCommand(StickId.ONE, target_position))

        return commands
