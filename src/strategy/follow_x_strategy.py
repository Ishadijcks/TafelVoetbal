from communication.commands.commands import BaseCommand, StickId
from communication.commands.translate_command import TranslateCommand
from model.game_state import GameState
from strategy.strategy import Strategy


class FollowXStrategy(Strategy):
    """
    Tries to place the keeper at the position of the ball
    """

    def __init__(self):
        super().__init__()

    def execute(self, previous_state: GameState, state: GameState, delta: float) -> list[BaseCommand]:
        # TODO convert between ball and keeper space


        prev_ball_x, prev_ball_y = state.ball
        ball_x, ball_y = state.ball

        prediction_x = ball_x + (ball_x - prev_ball_x)
        prediction_y = ball_y + (ball_y - prev_ball_y)

        clipped_ball = min(0.66, max(0.33, ball_y)) - 0.33

        target_position = clipped_ball / 0.33
        return [
            TranslateCommand(StickId.ONE, target_position),
        ]
