import simple_ast

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'
RETURN_OBJ = 'RETURN_VALUE'
ERROR = 'ERROR'
FUNCTION_OBJ = 'FUNCTION'

class Object():
    def type(): raise NotImplementedError('Subclass should implement type() function')
    def inspect(self): return f'{self.value}' 

class Integer(Object):
    def __init__(self, value: int): self.value = value
    def type(self): return INTEGER_OBJ

class Boolean(Object):
    def __init__(self, value: bool): self.value = value
    def type(self): return BOOLEAN_OBJ

class Null(Object):
    def inspect(self): return 'null'
    def type(self): return NULL_OBJ

class Return(Object):
    def __init__(self, value: Object): self.value = value
    def inspect(self): return self.value.inspect()
    def type(self): return RETURN_OBJ

class Error(Object):
    def __init__(self, message: str): self.message = message
    def inspect(self): return f'ERROR: {self.message}'
    def type(self): return ERROR

class Environment():
    def __init__(self, outer: "Environment" = None):
        self.environment: dict[str, Object] = {} 
        self.outer = outer

    def get(self, key: str) -> Object: 
        if key in self.environment: return self.environment[key]
        if self.outer is not None and key in self.outer.environment: return self.outer.environment[key]
        return None

    def set(self, key: str, value: Object): self.environment[key] = value    


class Function(Object):
    def __init__(self, parameters: list[simple_ast.Identifier], body: simple_ast.BlockStatement, environment: Environment):
        self.parameters = parameters
        self.body = body
        self.environment = environment

    def inspect(self): return f'fn ({''.join(parameter for parameter in self.parameters)}) {{{'\n'.join(statement for statement in self.body)}}}'
    def type(self): return FUNCTION_OBJ
