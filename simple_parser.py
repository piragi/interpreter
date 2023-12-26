import simple_ast
from simple_ast import Program
import simple_token
from simple_token import Lexer, Token

class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer 
        self.current_token: Token = None
        self.peek_token: Token = None
        self.errors = []

        self.next_token()
        self.next_token()    

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def parse_program(self) -> Program: 
        program = Program()
        
        while self.current_token.type is not simple_token.EOF:
            statement = self.parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self.next_token()

        return program

    def parse_statement(self):
        if self.current_token.type is simple_token.LET:
            return self.parse_let_statement()
        if self.current_token.type is simple_token.EOF:
            return None
    
    def parse_let_statement(self):
        statement = simple_ast.LetStatement(self.current_token, None, None)

        if not self.expect_peek(simple_token.IDENT):
            return None
        
        statement.name = simple_ast.Identifier(self.current_token, self.current_token.literal)

        if not self.expect_peek("ASSIGN"): # TODO: needs a token dict or something
            return None

        # skip expression for now
        while self.current_token.type != "SEMICOLON": # TODO: token dict or something
            self.next_token()
        
        return statement

    def expect_peek(self, expected: str):
        if self.peek_token.type is expected:
            self.next_token()
            return True
        else:
            self.peek_errors(expected)
            return False 

    def peek_errors(self, token_type):
        msg = f'expected next token to be {token_type}, got {self.peek_token.type} instead'
        self.errors.append(msg)
