from simple_token import Token

class Node():
    def token_literal():
        raise NotImplementedError("Subclasses should implement the token_literal method")

class Statement(Node):
    def __init__():
        pass
    
    def statemenetNode():
        raise NotImplementedError("Subclasses should implement the statementNode method")

class Expression(Node):
    def __init__():
        pass
    
    def expressionNode():
        raise NotImplementedError("Subclasses should implement the expressionNode method")

class Program():
    def __init__(self):
        self.statements = []

    def token_literal(self):
        if len(self.statemens > 0):
            return self.statements[0].token_literal()
        else:
            return ""


class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.token = token
        self.value = value

    def expressionNode():
        pass
    def token_literal(self):
        return self.value

class LetStatement(Statement):
    def __init__(self, token: Token, identifier: Identifier, expression: Expression):
        self.token = token
        self.name = identifier
        self.value = expression

    def statementNode():
        pass

    def token_literal(self):
        return self.token.literal