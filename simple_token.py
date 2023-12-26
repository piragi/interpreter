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
LPAREN    = "("
RPAREN    = ")"
LBRACE    = "{"
RBRACE    = "}"
ASSIGN    = "="
PLUS      = "+"
MINUS     = "-"
BANG      = "!"
ASTERISK  = "*"
SLASH     = "/"

LT = "<"
GT = ">"

EQ = "=="
NEQ = "!="

# keywords
FUNCTION = "FUNCTION"
LET = "LET"
TRUE = "TRUE"
FALSE = "FALSE"
IF = "IF"
ELSE = "ELSE"
RETURN = "RETURN"

KEYWORDS = {"fn": FUNCTION, "let": LET, "true": TRUE, "false": FALSE, "if": IF, "else": ELSE, "return": RETURN}

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
        else:
            self.char = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def next_token(self):
        self.skip_whitespaces()

        if self.char == "=":
            if self.peek_char() == "=":
                self.read_char()
                token = Token("EQ", "==")
            else:
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
        elif self.char == "-":
            token = Token("MINUS", "-")
        elif self.char == "!":
            if self.peek_char() == "=":
                self.read_char()
                token = Token("NEQ", "!=")
            else:
                token = Token("BANG", "!")
        elif self.char == "*":
            token = Token("ASTERISK", "*")
        elif self.char == "/":
            token = Token("SLASH", "/")
        elif self.char == "<":
            token = Token("LT", "<")
        elif self.char == ">":
            token = Token("GT", ">")
        elif self.char == "":
            token = Token("EOF", "")
        else:
            if self.char.isalpha():
                literal = self.read_literal()
                type = self.check_keyword(literal)
                return Token(type, literal)
            elif self.char.isnumeric():
                literal = self.read_number()
                return Token(INT, literal) 
            else:
                token = Token("ILLEGAL", self.char)
        self.read_char()
        return token

    def peek_char(self):
        if self.read_position >= len(self.input):
            return 0
        return self.input[self.read_position]

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