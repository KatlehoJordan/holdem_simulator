from src.guess_functions import clear_console
from src.simulate_and_aggregate import simulate_and_aggregate
from src.train import train
from src.graph import graph

# TODO: After getting all simulations and aggregations working, build a way to graph the results

# TODO: Get python debugger launch.json configuration working for a given file so that do not have to always bake logic into main.py


# TODO: Resolve TODOs in other files
def main(
    purpose: str = "Training",
) -> None:
    clear_console()
    if purpose == "Sim and Agg":
        simulate_and_aggregate()
    if purpose == "Training":
        train()
    if purpose == "Graph":
        graph()


if __name__ == "__main__":
    main(purpose="Graph")
