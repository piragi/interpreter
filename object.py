from typing import Callable
import simple_ast

INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'
RETURN_OBJ = 'RETURN_VALUE'
ERROR = 'ERROR'
FUNCTION_OBJ = 'FUNCTION'
STRING_OBJ = 'STRING'
BUILTIN_OBJ = 'BUILTIN'
ARRAY_OBJ = 'ARRAY'
HASH_OBJ = 'HASH'

class Object():
    def type(): raise NotImplementedError('Subclass should implement type() function')
    def inspect(self): return f'{self.value}'

class Integer(Object):
    def __init__(self, value: int): self.value = value
    def type(self): return INTEGER_OBJ
    def inspect(self): return str(self.value)
    def hashkey(self): return hash(('int', self.value))

class Boolean(Object):
    def __init__(self, value: bool): self.value = value
    def type(self): return BOOLEAN_OBJ
    def inspect(self): return str(self.value)
    def hashkey(self): return hash(('bool', self.value))

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

class Builtin(Object):
    def __init__(self, builtin: Callable[[list[Object]], Object]): self.builtin = builtin 
    def inspect(self): return 'builtin function'
    def type(self): BUILTIN_OBJ

class Function(Object):
    def __init__(self, parameters: list[simple_ast.Identifier], body: simple_ast.BlockStatement, environment: Environment):
        self.parameters = parameters
        self.body = body
        self.environment = environment

    def inspect(self): return f'fn ({''.join(parameter.inspect() for parameter in self.parameters)}) {{{'\n'.join(statement.inspect() for statement in self.body)}}}'
    def type(self): return FUNCTION_OBJ

class String(Object):
    def __init__(self, value: str): self.value = value
    def inspect(self): return self.value
    def type(self): return STRING_OBJ
    def hashkey(self): return hash(('str', self.value))

class Array(Object):
    def __init__(self, elements: list[simple_ast.Expression]): self.elements = elements
    def inspect(self): return f'[{', '.join(element.inspect() for element in self.elements)}]'
    def type(self): return ARRAY_OBJ

class HashPair():
    def __init__(self, key: Object, value: Object):
        self.key = key
        self.value = value
    
class Hash():
    def __init__(self): self.dict: dict[int, HashPair] = {}
    def type(self): return HASH_OBJ
    def inspect(self): return f'{{{', '.join(f'{hashpair.key.inspect()}: {hashpair.value.inspect()}' for _, hashpair in self.dict.items())}}}'

Hashable = Integer | Boolean | String