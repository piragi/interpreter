INTEGER_OBJ = 'INTEGER'
BOOLEAN_OBJ = 'BOOLEAN'
NULL_OBJ = 'NULL'
RETURN_OBJ = 'RETURN_VALUE'
ERROR = 'ERROR'

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
    def __init__(self): self.dictionary: dict[str, Object] = {}
    def get(self, key: str) -> Object: return self.dictionary[key] if key in self.dictionary else None #maybe different errorhandling?
    def set(self, key: str, value: Object): self.dictionary[key] = value
