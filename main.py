from src.guess_functions import clear_console
from src.plot_data import plot_data
from src.simulate_and_aggregate import simulate_and_aggregate
from src.train import train


# TODO: Get python debugger launch.json configuration working for a given file so that do not have to always bake logic into main.py
# TODO: Resolve TODOs in other files
def main(
    purpose: str = "Training",
) -> None:
    clear_console()
    if purpose == "Sim and Agg":
        for n_players in [*range(10, 11)]:
            simulate_and_aggregate(n_players_per_simulation=n_players)
    if purpose == "Training":
        # TODO: remove next line when done troubleshooting specific n-players
        # train(n_players_ahead_of_you=9)
        train()
    if purpose == "Plot":
        plot_data(show_plot=True)


if __name__ == "__main__":
    # TODO: Remove older uses of main()
    # main(purpose="Sim and Agg")
    main(purpose="Training")
