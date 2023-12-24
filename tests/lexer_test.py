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

let result = add(five, ten);
!-/*5;
5 < 10 > 5;
if (5 < 10) {
    return true;
} else {
    return false;
}

10 == 10;
10 != 9;
"""
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
        Token("BANG", "!"),
        Token("MINUS", "-"),
        Token("SLASH", "/"),
        Token("ASTERISK", "*"),
        Token("INT", "5"),
        Token("SEMICOLON", ";"),
        Token("INT", "5"),
        Token("LT", "<"),
        Token("INT", "10"),
        Token("GT", ">"),
        Token("INT", "5"),
        Token("SEMICOLON", ";"),
        Token("IF", "if"),
        Token("LPAREN", "("),
        Token("INT", "5"),
        Token("LT", "<"),
        Token("INT", "10"),
        Token("RPAREN", ")"),
        Token("LBRACE", "{"),
        Token("RETURN", "return"),
        Token("TRUE", "true"),
        Token("SEMICOLON", ";"),
        Token("RBRACE", "}"),
        Token("ELSE", "else"),
        Token("LBRACE", "{"),
        Token("RETURN", "return"),
        Token("FALSE", "false"),
        Token("SEMICOLON", ";"),
        Token("RBRACE", "}"),
        Token("INT", "10"),
        Token("EQ", "=="),
        Token("INT", "10"),
        Token("SEMICOLON", ";"),
        Token("INT", "10"),
        Token("NEQ", "!="),
        Token("INT", "9"),
        Token("SEMICOLON", ";"),
        Token("EOF", ""),
    ]

    assert_tokens(input, assert_input)

