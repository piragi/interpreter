import simple_ast
from simple_ast import Program
import simple_token
from simple_token import Lexer, Token

PRECEDENCE = {"_": 0, "LOWEST": 1, "EQUALS": 2, "LESSGREATER": 3, "SUM": 4, "PRODUCT": 5, "PREFIX": 6, "CALL": 7}
OP_PRECEDENCES = {"EQ": "EQUALS", "NEQ": "EQUALS", "LT": "LESSGREATER", "GT": "LESSGREATER", "MINUS": "SUM", "PLUS": "SUM", "SLASH": "PRODUCT", "ASTERISK": "PRODUCT"}

class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer 
        self.current_token: Token = None
        self.peek_token: Token = None
        self.errors = []
        self.prefix_parse_fn = {}
        self.infix_parse_fn = {}
        
        self.register_prefix("IDENT", self.parse_identifier)
        self.register_prefix("INT", self.parse_integer_literal)
        self.register_prefix("BANG", self.parse_prefix_expression)
        self.register_prefix("MINUS", self.parse_prefix_expression)

        self.register_infix("EQ", self.parse_infix_expression)
        self.register_infix("NEQ", self.parse_infix_expression)
        self.register_infix("LT", self.parse_infix_expression)
        self.register_infix("GT", self.parse_infix_expression)
        self.register_infix("MINUS", self.parse_infix_expression)
        self.register_infix("PLUS", self.parse_infix_expression)
        self.register_infix("SLASH", self.parse_infix_expression)
        self.register_infix("ASTERISK", self.parse_infix_expression)

        self.next_token()
        self.next_token()    

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def register_prefix(self, token: Token, fn: callable):
        self.prefix_parse_fn[token] = fn

    def register_infix(self, token: Token, fn: callable):
        self.infix_parse_fn[token] = fn

    def parse_program(self) -> Program: 
        program = Program()
        
        while self.current_token.type is not "EOF":
            statement = self.parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self.next_token()

        return program

    def parse_statement(self):
        if self.current_token.type is "LET":
            return self.parse_let_statement()
        elif self.current_token.type is "RETURN":
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self):
        statement = simple_ast.LetStatement(self.current_token, None, None)

        if not self.expect_peek("IDENT"):
            return None
        
        statement.name = simple_ast.Identifier(self.current_token, self.current_token.literal)

        if not self.expect_peek("ASSIGN"): # TODO: needs a token dict or something
            return None

        # skip expression for now
        while self.current_token.type != "SEMICOLON": # TODO: token dict or something
            self.next_token()
        
        return statement

    def parse_return_statement(self):
        statement = simple_ast.ReturnStatement(self.current_token)
        self.next_token()
        
        # skip expression for now
        while self.current_token.type != "SEMICOLON": # TODO: token dict or something
            self.next_token()
        
        return statement
    
    def parse_expression_statement(self):
        statement = simple_ast.ExpressionStatement(self.current_token)
        statement.expression = self.parse_expression(PRECEDENCE.get("LOWEST"))

        if self.peek_token.type == "SEMICOLON":
            self.next_token()
        return statement
    
    def parse_identifier(self):
        return simple_ast.Identifier(self.current_token, self.current_token.literal)
    
    def parse_integer_literal(self):
        # TODO: wrap in try, if integer cannot be converted to int add error
        literal = simple_ast.IntegerLiteral(self.current_token, int(self.current_token.literal))
        return literal

    def parse_expression(self, precedence: int):
        if self.current_token.type not in self.prefix_parse_fn:
            self.no_prefix_parse_fn_error(self.current_token.type)
            return None
        prefix = self.prefix_parse_fn[self.current_token.type]

        left_expression = prefix()

        while self.peek_token.type != "SEMICOLON" and precedence < self.peek_precedence():
            if self.peek_token.type not in self.infix_parse_fn:
                return left_expression
            infix = self.infix_parse_fn[self.peek_token.type]
            self.next_token()
            left_expression = infix(left_expression)

        return left_expression
    
    def parse_prefix_expression(self):
        expression = simple_ast.PrefixExpression(self.current_token, self.current_token.literal)
        self.next_token()
        expression.right = self.parse_expression(PRECEDENCE["PREFIX"])
        return expression
    
    def parse_infix_expression(self, left: simple_ast.Expression):
        expression = simple_ast.InfixExpression(self.current_token, left, self.current_token.literal)
        precedence = self.current_precedence()
        self.next_token()
        expression.right = self.parse_expression(precedence)
        return expression

    def expect_peek(self, expected: str):
        if self.peek_token.type is expected:
            self.next_token()
            return True
        else:
            self.peek_errors(expected)
            return False 
    
    def peek_precedence(self):
        if self.peek_token.type in OP_PRECEDENCES:
            return PRECEDENCE[OP_PRECEDENCES[self.peek_token.type]]
        return PRECEDENCE["LOWEST"]

    def current_precedence(self):
        if self.current_token.type in OP_PRECEDENCES:
            return PRECEDENCE[OP_PRECEDENCES[self.current_token.type]]
        return PRECEDENCE["LOWEST"]

    def peek_errors(self, token_type):
        msg = f'expected next token to be {token_type}, got {self.peek_token.type} instead'
        self.errors.append(msg)

    def no_prefix_parse_fn_error(self, token_type: str):
        msg = f'no prefix parse function for {token_type} found'
        self.errors.append(msg)