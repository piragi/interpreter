ILLEGAL = "ILLEGAL"
EOF = "EOF"
# identifiers
IDENT = "IDENT"
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

KEYWORDS = {"fn": FUNCTION, "let": LET}

class Lexer:
    def __init__(self, input:str):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.char = 0

        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.char = ""
            return
        self.char = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        self.skip_whitespaces()

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
        elif self.char == "":
            token = Token("EOF", "")
        else:
            if self.char.isalpha():
                literal = self.read_literal()
                # TODO: this return is weird
                type = self.check_keyword(literal)
                return Token(type, literal)
            elif self.char.isnumeric():
                literal = self.read_number()
                return Token(INT, literal) 
            else:
                token = Token("ILLEGAL", self.char)
        self.read_char()
        return token

    def read_literal(self):
        literal_start = self.position
        while self.char.isalpha() or self.char == "_":
            self.read_char()
        return self.input[literal_start:self.position]
    
    def read_number(self):
        literal_start = self.position
        while self.char.isnumeric():
            self.read_char()
        return self.input[literal_start:self.position]
    
    def check_keyword(self, literal):
        if literal in KEYWORDS:
            return KEYWORDS[literal]
        return IDENT

    def skip_whitespaces(self):
        while self.char.isspace():
            self.read_char()

class Token:
    def __init__(self, type: str, literal: str):
        self.type = type
        self.literal = literal


        

