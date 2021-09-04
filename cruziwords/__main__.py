import argparse
import logging
from argparse import ArgumentParser
from pathlib import Path

from .examples import random_example
from .scoring import score_puzzle
from .search import search_puzzle
from .view.cli import print_solution
from .words import WordsCorpus

LOGGER = logging.getLogger(__file__)


def parse_args() -> argparse.Namespace:
    argp = ArgumentParser("Cruziwords crosswords puzzle generator!")
    argp.add_argument(
        "csv_path", nargs="?", type=Path, default=random_example(), help="CSV file containing word definitions"
    )
    argp.add_argument("--max-iterations", type=int, help="Number of parallel random searches")
    return argp.parse_args()


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    args = parse_args()

    csv_path = args.csv_path
    words = WordsCorpus.from_csv_file(csv_path)
    LOGGER.debug("%d words loaded from %s", len(words), csv_path)

    LOGGER.debug("Beginning search, max iterations: %s", args.max_iterations)
    winning_puzzle = search_puzzle(words, score_puzzle, args.max_iterations)
    print_solution(winning_puzzle)
