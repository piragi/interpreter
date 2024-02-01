import simple_ast, object as obj
import simple_builtins

NULL = obj.Null()
TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)

#TODO: this does not need to be a class
class Evaluator():
    def eval(self, node: simple_ast.Node, environment: obj.Environment):
        if type(node) == simple_ast.Program: return self.eval_statements(node.statements, environment)
        if type(node) == simple_ast.ExpressionStatement: return self.eval(node.expression, environment)
        if type(node) == simple_ast.IntegerLiteral: return obj.Integer(node.value)
        if type(node) == simple_ast.Boolean: return self.native_bool_to_object(node.value)
        if type(node) == simple_ast.PrefixExpression: return self.eval_prefix_expression(node.operator, self.eval(node.right, environment))
        if type(node) == simple_ast.InfixExpression: return self.eval_infix_expression(node.operator, self.eval(node.left, environment), self.eval(node.right, environment))
        if type(node) == simple_ast.BlockStatement: return self.eval_block_statements(node.statements, environment)
        if type(node) == simple_ast.IfExpression: return self.eval_if_expression(node, environment)
        if type(node) == simple_ast.ReturnStatement: return self.eval_return_statement(self.eval(node.value, environment))
        if type(node) == simple_ast.LetStatement: self.eval_let_statement(node, environment)
        if type(node) == simple_ast.Identifier: return self.eval_identifiers(node, environment)
        if type(node) == simple_ast.FunctionLiteral: return self.eval_function_literal(node, environment)
        if type(node) == simple_ast.CallExpression: return self.eval_call_expression(node, environment)
        if type(node) == simple_ast.StringLiteral: return obj.String(node.value)
        if type(node) == simple_ast.ArrayLiteral: return self.eval_array_literals(node, environment)
        if type(node) == simple_ast.IndexExpression: return self.eval_index_expression(node, environment)
        if type(node) == simple_ast.HashLiteral: return self.eval_hash_literal(node, environment)
        return None 

    def eval_statements(self, statements: list[simple_ast.Statement], environment: obj.Environment):
        for statement in statements:
            result = self.eval(statement, environment)
            if type(result) == obj.Return: return result.value
            if type(result) == obj.Error: return result
        return result
    
    def eval_block_statements(self, statemenets: list[simple_ast.Statement], environment: obj.Environment):
        for statement in statemenets:
            result = self.eval(statement, environment)
            if type(result) == obj.Return or type(result) == obj.Error: return result
        return result
    
    def eval_function_literal(self, node: simple_ast.FunctionLiteral, environment: obj.Environment):
        params = node.parameters
        body = node.body
        return obj.Function(params, body, environment)
    
    def eval_call_expression(self, node: simple_ast.CallExpression, environment: obj.Environment):
        function = self.eval(node.function, environment)
        if self.is_error(function): return function
        args = self.eval_expressions(node.arguments, environment)
        if len(args) == 1 and self.is_error(args[0]): return args[0]
        return self.apply_function(function, args)
    
    def eval_expressions(self, args: list[simple_ast.Expression], environment: obj.Environment):
        result: list[obj.Object] = []
        for argument in args:
            evaluated = self.eval(argument, environment)
            if self.is_error(evaluated): return evaluated
            result.append(evaluated)
        return result
    
    def eval_hash_literal(self, node: simple_ast.HashLiteral, environment: obj.Environment):
        hash_dict = obj.Hash()
        for key_node, value_node in node.dict.items():
            key = self.eval(key_node, environment)
            if self.is_error(key): return key
            if not isinstance(key, obj.Hashable): return self.new_error(f'object type not supported for key, got={key.type()}')
            key_hash = key.hashkey()
            value = self.eval(value_node, environment)
            if self.is_error(value): return value

            hash_dict.dict[key_hash] = obj.HashPair(key, value)
        return hash_dict
    
    def eval_array_literals(self, node: simple_ast.ArrayLiteral, environment: obj.Environment):
        elements = self.eval_expressions(node.elements, environment)
        if len(elements) == 1 and self.is_error(elements[0]): return elements[0]
        return obj.Array(elements)

    def eval_index_expression(self, node: simple_ast.IndexExpression, environment: obj.Environment):
        left = self.eval(node.left, environment)
        if self.is_error(left): return left
        index = self.eval(node.index, environment)
        if self.is_error(index): return index
        if type(left) == obj.Array and type(index) == obj.Integer: return self.eval_index_array_expression(left, index)
        if type(left) == obj.Hash and isinstance(index, obj.Hashable): return self.eval_index_hash_expression(left, index)
        return self.new_error(f'index operator not supported: {left.type()}')
    
    def eval_index_array_expression(self, array: obj.Array, index: obj.Integer):
        max = len(array.elements)
        print(f'array={len(array.elements)}, index={index.value}')
        if index.value < 0 or index.value >= max: return None
        return array.elements[index.value]
    
    def eval_index_hash_expression(self, hash_dict: obj.Hash, index: obj.Hashable):
        pair = hash_dict.dict.get(index.hashkey())
        if pair is None: return NULL
        return pair.value
    
    def apply_function(self, function: obj.Object, args: list[obj.Object]):
        if type(function) == obj.Function:
            extended_environment = self.extended_function_environment(function, args)
            evaluated = self.eval(function.body, extended_environment)
            return self.unwrapped_return_value(evaluated)
        if type(function) == obj.Builtin: return function.builtin(args) 
        else: return self.new_error(f'not a function: {function.type()}') 
    
    def extended_function_environment(self, function: obj.Function, args: list[obj.Object]):
        environment = obj.Environment(function.environment)
        for i, parameter in enumerate(function.parameters): 
            environment.set(parameter.value, args[i]) 
        return environment
    
    def unwrapped_return_value(self, return_value: obj.Object):
        if type(return_value) == obj.Return: return return_value.value 
        return return_value

    def eval_let_statement(self, node: simple_ast.LetStatement, environment: obj.Environment):
        value = self.eval(node.value, environment)
        if self.is_error(value): return value 
        environment.set(node.name.value, value)
    
    def eval_identifiers(self, node: simple_ast.Identifier, environment: obj.Environment):
        value = environment.get(node.value) 
        if value is None: value = simple_builtins.functions.get(node.value)
        if value is None: return self.new_error(f'identifier not found: {node.value}')
        
        return value
    
    def native_bool_to_object(self, boolean): return TRUE if boolean else FALSE

    def eval_prefix_expression(self, operator: str, right: obj.Object):
        if self.is_error(right): return right
        if operator == "!": return self.eval_bang_operator_expression(right)
        if operator == "-": return self.eval_minus_operator_expression(right)
        return self.new_error(f'unknown operator: {operator}{right.type()}')
    
    def eval_bang_operator_expression(self, object: obj.Object):
        if object == TRUE: return FALSE
        if object == FALSE: return TRUE
        if object == NULL: return TRUE 
        return FALSE
    
    def eval_minus_operator_expression(self, object: obj.Object):
        if type(object) != obj.Integer: return self.new_error(f'unknown operator: -{object.type()}')
        object.value = -object.value
        return object
    
    def eval_infix_expression(self, operator: str, left: obj.Object, right: obj.Object):
        if self.is_error(left): return left
        if self.is_error(right): return right
        if type(left) == obj.Integer and type(right) == obj.Integer: return self.eval_infix_integer_expression(operator, left, right)
        if type(left) == obj.Boolean and type(right) == obj.Boolean: return self.eval_infix_boolean_expression(operator, left, right)
        if type(left) == obj.String and type(right) == obj.String: return self.eval_infix_string_expression(operator, left, right)
        return self.new_error(f'type mismatch: {left.type()} {operator} {right.type()}')
    
    def eval_infix_string_expression(self, operator: str, left: obj.String, right: obj.String):
        if operator == "+": return obj.String(f'{left.value}{right.value}')
        return self.new_error(f'unknown operator: {left.type()} {operator} {right.type()}')
    
    def eval_infix_boolean_expression(self, operator: str, left: obj.Boolean, right: obj.Boolean):
        if operator == "==": return self.native_bool_to_object(left == right)
        if operator == "!=": return self.native_bool_to_object(left != right)
        return self.new_error(f'unknown operator: {left.type()} {operator} {right.type()}')
    
    def eval_infix_integer_expression(self, operator: str, left: obj.Integer, right: obj.Integer):
        if operator == "+": return obj.Integer(left.value + right.value)
        if operator == "-": return obj.Integer(left.value - right.value)
        if operator == "*": return obj.Integer(left.value * right.value)
        if operator == "/": return obj.Integer(left.value / right.value)
        if operator == "<": return self.native_bool_to_object(left.value < right.value)
        if operator == ">": return self.native_bool_to_object(left.value > right.value)
        if operator == "==": return self.native_bool_to_object(left.value == right.value)
        if operator == "!=": return self.native_bool_to_object(left.value != right.value)
        return self.new_error(f'unknown operator: {left.type()} {operator} {right.type()}')
    
    def eval_if_expression(self, if_expression: simple_ast.IfExpression, environment: obj.Environment):
        condition = self.eval(if_expression.condition, environment)
        if self.is_truthy(condition): return self.eval(if_expression.consequence, environment)
        elif if_expression.alternative is not None: return self.eval(if_expression.alternative, environment) 
        return NULL
    
    def eval_return_statement(self, object: obj.Object):
        if self.is_error(object): return object 
        return obj.Return(object)

    def is_truthy(self, condition: obj.Boolean):
        if condition == NULL: return False
        if condition == FALSE: return False
        if condition == TRUE: return True
        return True

    def new_error(self, message: str): return obj.Error(message)

    def is_error(self, object: obj.Object): 
        if object.type() == obj.ERROR or object is None: return True
        else: False
