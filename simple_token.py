ILLEGAL = "ILLEGAL"
EOF = "EOF"
# identifiers
IDENT = "IDENTIFIER"
INT = "INT"
# operators
ASSIGN = "="
PLUS = "+"
# delimiters
COMMA = ","
SEMICOLON = ";"
LPAREN = "("
RPAREN = ")"
LBRACE = "{"
RBRACE = "}"
# keywords
FUNCTION = "FUNCTION"
LET = "LET"


class Lexer:
    def __init__(self, input:str):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.char = 0

        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.char = 0
            return
        self.char = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        if self.char == "=":
            token = Token("ASSIGN", "=")
        elif self.char == "+":
            token = Token("PLUS", "+")
        elif self.char == "(":
            token = Token("LPAREN", "(")
        elif self.char == ")":
            token = Token("RPAREN", ")")
        elif self.char == "{":
            token = Token("LBRACE", "{")
        elif self.char == "}":
            token = Token("RBRACE", "}")
        elif self.char == ",":
            token = Token("COMMA", ",")
        elif self.char == ";":
            token = Token("SEMICOLON", ";")
        else:
            token = Token("EOF", "")
        self.read_char()
        return token

class Token:
    def __init__(self, type: str, literal: str):
        self.type = type
        self.literal = literal


        

