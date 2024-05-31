from input_reader import read_input
from fight import zip_steps, fight_loop, Player
from constants import PLAYER_1, PLAYER_2

EXAMPLES = ["ejemplo_1", "ejemplo_2_j1", "ejemplo_3_j2"]


def main(input_file: str = EXAMPLES[0]):
    input_dict = read_input(input_file)

    steps = zip_steps(input_dict=input_dict)

    player_1 = Player(data=PLAYER_1)
    player_2 = Player(data=PLAYER_2)
    fight_loop(steps=steps, player_1=player_1, player_2=player_2)


if __name__ == "__main__":
    main(input_file=EXAMPLES[0])
