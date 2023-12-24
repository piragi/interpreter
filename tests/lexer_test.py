import sys
from pathlib import Path

root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from simple_token import Lexer, Token

def assert_tokens(input, assert_input):
    lexer = Lexer(input)

    for assert_token in assert_input:
        token = lexer.next_token()
        assert token.type == assert_token.type
        assert token.literal == assert_token.literal

def test_operators():
    input = "=+(){},;"
    assert_input = [Token("ASSIGN", "="), Token("PLUS", "+"), Token("LPAREN", "("), Token("RPAREN", ")"), Token("LBRACE", "{"), Token("RBRACE", "}"), Token("COMMA", ","), Token("SEMICOLON", ";")]
    assert_tokens(input, assert_input)

def test_add():
    input = """let five = 5;
let ten = 10;

let add = fn(x, y) {
  x + y;
};

let result = add(five, ten);"""
    assert_input = [Token("LET", "let"),
        Token("IDENT", "five"),
        Token("ASSIGN", "="),
        Token("INT", "5"),
        Token("SEMICOLON", ";"),
        Token("LET", "let"),
        Token("IDENT", "ten"),
        Token("ASSIGN", "="),
        Token("INT", "10"),
        Token("SEMICOLON", ";"),
        Token("LET", "let"),
        Token("IDENT", "add"),
        Token("ASSIGN", "="),
        Token("FUNCTION", "fn"),
        Token("LPAREN", "("),
        Token("IDENT", "x"),
        Token("COMMA", ","),
        Token("IDENT", "y"),
        Token("RPAREN", ")"),
        Token("LBRACE", "{"),
        Token("IDENT", "x"),
        Token("PLUS", "+"),
        Token("IDENT", "y"),
        Token("SEMICOLON", ";"),
        Token("RBRACE", "}"),
        Token("SEMICOLON", ";"),
        Token("LET", "let"),
        Token("IDENT", "result"),
        Token("ASSIGN", "="),
        Token("IDENT", "add"),
        Token("LPAREN", "("),
        Token("IDENT", "five"),
        Token("COMMA", ","),
        Token("IDENT", "ten"),
        Token("RPAREN", ")"),
        Token("SEMICOLON", ";"),
        Token("EOF", ""),
    ]

    assert_tokens(input, assert_input)

