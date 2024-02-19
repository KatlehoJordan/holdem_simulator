import logging

MIN_SMALL_BLIND = 10
SMALL_BLIND_INCREMENT = 5
MAX_SMALL_BLIND = 100
MIN_PLAYERS_AHEAD_OF_YOU = 1
MAX_PLAYERS_AHEAD_OF_YOU = 9

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()
