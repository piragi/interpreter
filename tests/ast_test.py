import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import pytest
import simple_token
import simple_parser

@pytest.mark.skip(reason="no way of currently testing this")
def test_string():
    test_input = """let myvar = anothervar;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    assert program.string() == "let myvar = anothervar;"