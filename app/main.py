from input_reader import read_input
from fight import zip_steps

EXAMPLES = [
    "ejemplo_1", "ejemplo_2_j1", "ejemplo_3_j2"
]

def main(input_file:str=EXAMPLES[0]):
    input_dict = read_input(input_file)

    steps = zip_steps(input_dict=input_dict)

if __name__ == "__main__":
    main(input_file=EXAMPLES[0])