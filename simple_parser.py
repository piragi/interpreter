import simple_ast
from simple_ast import Program
import simple_token
from simple_token import Lexer, Token

PRECEDENCE = {"_": 0, "LOWEST": 1, "EQUALS": 2, "LESSGREATER": 3, "SUM": 4, "PRODUCT": 5, "PREFIX": 6, "CALL": 7, "INDEX": 8}
OP_PRECEDENCES = {"EQ": "EQUALS", "NEQ": "EQUALS", "LT": "LESSGREATER", "GT": "LESSGREATER", "MINUS": "SUM", "PLUS": "SUM", "SLASH": "PRODUCT", "ASTERISK": "PRODUCT", "LPAREN": "CALL", "LBRACKET": "INDEX"}

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
        self.register_prefix("TRUE", self.parse_boolean)
        self.register_prefix("FALSE", self.parse_boolean)
        self.register_prefix("LPAREN", self.parse_grouped_expression)
        self.register_prefix("IF", self.parse_if_expression)
        self.register_prefix("FUNCTION", self.parse_function_literal)
        self.register_prefix("STRING", self.parse_string_literal)
        self.register_prefix("LBRACKET", self.parse_array_literal)

        self.register_infix("EQ", self.parse_infix_expression)
        self.register_infix("NEQ", self.parse_infix_expression)
        self.register_infix("LT", self.parse_infix_expression)
        self.register_infix("GT", self.parse_infix_expression)
        self.register_infix("MINUS", self.parse_infix_expression)
        self.register_infix("PLUS", self.parse_infix_expression)
        self.register_infix("SLASH", self.parse_infix_expression)
        self.register_infix("ASTERISK", self.parse_infix_expression)
        self.register_infix("LPAREN", self.parse_call_expression)
        self.register_infix("LBRACKET", self.parse_index_expression)

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
        
        while self.current_token.type != "EOF":
            statement = self.parse_statement()
            if statement is not None:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self):
        if self.current_token.type == "LET":
            return self.parse_let_statement()
        elif self.current_token.type == "RETURN":
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()
    
    def parse_let_statement(self):
        statement = simple_ast.LetStatement(self.current_token, None, None)

        if not self.expect_peek("IDENT"): return None
        statement.name = simple_ast.Identifier(self.current_token, self.current_token.literal)
        if not self.expect_peek("ASSIGN"): return None
        self.next_token()
        statement.value = self.parse_expression(PRECEDENCE["LOWEST"])
        if self.peek_token.type == "SEMICOLON": self.next_token()
        return statement

    def parse_return_statement(self):
        statement = simple_ast.ReturnStatement(self.current_token)
        self.next_token()
        statement.value = self.parse_expression(PRECEDENCE["LOWEST"])
        if self.peek_token.type == "SEMICOLON": self.next_token()
        return statement
    
    def parse_expression_statement(self):
        statement = simple_ast.ExpressionStatement(self.current_token)
        statement.expression = self.parse_expression(PRECEDENCE.get("LOWEST"))

        if self.peek_token.type == "SEMICOLON":
            self.next_token()
        return statement
    
    #TODO: errorhandling for type conversion into int
    def parse_integer_literal(self): return simple_ast.IntegerLiteral(self.current_token, int(self.current_token.literal))
    def parse_identifier(self): return simple_ast.Identifier(self.current_token, self.current_token.literal)
    def parse_string_literal(self): return simple_ast.StringLiteral(self.current_token, self.current_token.literal)

    def parse_array_literal(self):
        array = simple_ast.ArrayLiteral(self.current_token)
        array.elements = self.parse_expression_list("RBRACKET")
        return array
    
    def parse_expression_list(self, token_type: str):
        expressions = [] #TODO: add typing
        if self.peek_token.type == token_type:
            self.next_token()
            return expressions
        
        self.next_token()
        expressions.append(self.parse_expression(PRECEDENCE["LOWEST"]))
        while self.peek_token.type == "COMMA":
            self.next_token()
            self.next_token()
            expressions.append(self.parse_expression(PRECEDENCE["LOWEST"]))
        if not self.expect_peek(token_type): return None
        return expressions

    def parse_index_expression(self, left: simple_ast.Expression):
        index_expression = simple_ast.IndexExpression(self.current_token, left)
        self.next_token()
        index_expression.index = self.parse_expression(PRECEDENCE["LOWEST"])
        if not self.expect_peek("RBRACKET"): return None
        return index_expression

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
    
    def parse_boolean(self): return simple_ast.Boolean(self.current_token, self.current_token.type == simple_token.TRUE)

    def parse_grouped_expression(self):
        self.next_token()
        expression = self.parse_expression(PRECEDENCE["LOWEST"])
        if not self.expect_peek("RPAREN"): return None
        return expression
    
    def parse_if_expression(self):
        expression = simple_ast.IfExpression(self.current_token) 
        if not self.expect_peek("LPAREN"): return None
        self.next_token()
        expression.condition = self.parse_expression(PRECEDENCE["LOWEST"])

        if not self.expect_peek("RPAREN"): return None
        if not self.expect_peek("LBRACE"): return None
        expression.consequence = self.parse_block_statement()

        if self.peek_token.type == "ELSE":
            self.next_token()
            if not self.expect_peek("LBRACE"): return None
            expression.alternative = self.parse_block_statement()
        return expression

    def parse_block_statement(self):
        block_statements = simple_ast.BlockStatement(self.current_token)
        self.next_token()

        while self.current_token.type != "RBRACE" and self.current_token.type != "EOF":
            statement = self.parse_statement()
            if statement is not None: block_statements.statements.append(statement)
            self.next_token()
        return block_statements
    
    def parse_function_literal(self):
        function_literal = simple_ast.FunctionLiteral(self.current_token)
        if not self.expect_peek("LPAREN"): return None
        function_literal.parameters = self.parse_function_parameters()
        if not self.expect_peek("LBRACE"): return None
        function_literal.body = self.parse_block_statement()
        return function_literal

    def parse_function_parameters(self):
        identifiers = []

        if self.peek_token.type == "RPAREN": 
            self.next_token()
            return identifiers

        self.next_token()
        identifiers.append(self.parse_identifier())
        while self.peek_token.type == "COMMA":
            self.next_token()
            self.next_token()
            identifiers.append(self.parse_identifier())
        if not self.expect_peek("RPAREN"): return None
        return identifiers
    
    def parse_call_expression(self, function):
        expression = simple_ast.CallExpression(self.current_token, function)
        expression.arguments = self.parse_expression_list("RPAREN")
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