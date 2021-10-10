from markupsafe import escape
from mako.template import Template

from ..puzzle import Direction, Letter, Puzzle, SquareType, WordStart
from ..words import Word

ColorType = tuple[int, int, int]


def color_word(word: Word) -> ColorType:
    r = 200 + hash(word.solution) % 50
    g = 200 + hash(word.solution + "1") % 50
    b = 200 + hash(word.solution + "2") % 50
    return r, g, b


def avg_colors(colors: list[ColorType]) -> ColorType:
    return tuple(int(sum(color[i] for color in colors) / len(colors)) for i in (0, 1, 2))  # type: ignore


def color(*words: Word) -> str:
    """
    Assign a random color to each word.
    :param words: One or more words.
    :return: Random color string suitable for use in CSS.
    """
    r, g, b = avg_colors([color_word(word) for word in words])
    return f"rgb({r}, {g}, {b})"


def render_square(square: SquareType) -> str:
    match square:
        case WordStart(dir=dir, word=word):
            return f'''<td class="word_start" title="{escape(word.clue)}" style="background-color: {color(word)}">
                {"&#9654; " if dir == Direction.ACROSS else "&#9660; "} {escape(word.clue)}
            </td>'''
        case Letter(words=words):
            return f'<td class="letter" style="background-color: {color(*words)}"><input type="text"/></td>'
        case _:
            return '<td class="empty"></td>'


def render_puzzle(puzzle: Puzzle) -> str:
    template = Template(filename="cruziwords/view/template.html")

    rows = [
        [puzzle[col, row] for col in range(puzzle.left, puzzle.right + 1)]
        for row in range(puzzle.top, puzzle.bottom + 1)
    ]

    return str(template.render(rows=rows, color=color, render_square=render_square))
