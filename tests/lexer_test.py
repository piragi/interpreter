import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

import simple_token

def test_next_token():
    input = "=+(){},;"
    assert_input = ["ASSIGN", "PLUS", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMA", "SEMICOLON"]


    lexer = simple_token.Lexer(input)
    print(lexer.char)

    for assert_token in assert_input:
        token = lexer.next_token()
        assert token.type == assert_token