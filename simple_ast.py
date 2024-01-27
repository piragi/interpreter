from simple_token import Token

class Node():
    def token_literal(): raise NotImplementedError("Subclasses should implement the token_literal method")
    def string(): raise NotImplementedError("Subclasses should implement the string method")

class Statement(Node):
    def statemenetNode(): raise NotImplementedError("Subclasses should implement the statementNode method")

class Expression(Node): 
    def expressionNode(): raise NotImplementedError("Subclasses should implement the expressionNode method")

class Program():
    def __init__(self):
        self.statements = []

    def token_literal(self):
        if len(self.statemens > 0):
            return self.statements[0].token_literal()
        else:
            return ""
        
    def string(self):
        statement_str = ""
        for statement in self.statements:
            statement_str += statement.string()
        return statement_str


class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self): return self.value

class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, expression: Expression):
        self.token = token
        self.name = identifier
        self.value = expression

    def statementNode(): pass
    def token_literal(self): return self.token.literal
    
    def string(self):
        out = f'{self.token_literal()}: {self.name.string()} = '
        if self.value is not None:
            out += self.value.string()
        out += ";"
        return out

class ReturnStatement(Statement):
    def __init__(self, token: Token, expression: Expression = None):
        self.token = token
        self.expression = expression
    
    def statementNode(): pass
    def token_literal(self): return self.token.literal

    def string(self):
        out = f'{self.token_literal()} '
        if self.expression is not None:
            out += self.expression.string()
        out += ";"
        return out
    
class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression: Expression = None):
        self.token = token
        self.expression = expression

    def statemenetNode(): pass        
    def token_literal(self): return self.token.literal
    
    def string(self):
        if self.expression is not None:
            return self.expression.string()
        return ""

class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int = None):
        self.token = token
        self.value = value

    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self): return self.token.literal

class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str = None, right: Expression = None):
        self.token = token
        self.operator = operator
        self.right = right
    
    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self): return f'({self.operator}{self.right.string()})'

class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression = None, operator: str = None, right: Expression = None):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right
    
    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self): return f'({self.left.string()} {self.operator} {self.right.string()})'

class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.token = token
        self.value = value
    
    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self): return self.token.literal

class BlockStatement(Statement):
    def __init__(self, token: Token):
        self.token = token #{ token
        self.statements = []
    
    def statemenetNode(): pass
    def token_literal(self): self.token.literal
    def string(self): return ''.join(statement.string() for statement in self.statements)

class IfExpression(Expression):
    def __init__(self, token: Token):
        self.token = token
        self.condition: Expression = None
        self.consequence: BlockStatement = None
        self.alternative: BlockStatement = None

    def expressionNode(): pass
    def token_literal(self): return self.token.literal
    def string(self):
        string = f'if {self.condition.string()} {self.consequence.string()}'
        if self.alternative is not None:
            string += f'else {self.alternative.string()}'
        return string