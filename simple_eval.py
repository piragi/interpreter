import simple_ast, object as obj

NULL = obj.Null()
TRUE = obj.Boolean(True)
FALSE = obj.Boolean(False)

class Evaluator():
    def eval(self, node: simple_ast.Node) -> obj.Object:
        if type(node) == simple_ast.Program: return self.eval_statements(node.statements)
        if type(node) == simple_ast.ExpressionStatement: return self.eval(node.expression)
        if type(node) == simple_ast.IntegerLiteral: return obj.Integer(node.value)
        if type(node) == simple_ast.Boolean: return self.native_bool_to_object(node.value)
        if type(node) == simple_ast.PrefixExpression: return self.eval_prefix_expression(node.operator, self.eval(node.right))
        if type(node) == simple_ast.InfixExpression: return self.eval_infix_expression(node.operator, self.eval(node.left), self.eval(node.right))
        if type(node) == simple_ast.BlockStatement: return self.eval_block_statements(node.statements)
        if type(node) == simple_ast.IfExpression: return self.eval_if_expression(node)
        if type(node) == simple_ast.ReturnStatement: return self.eval_return_statement(self.eval(node.value))
        return None 

    def eval_statements(self, statements: list[simple_ast.Statement]):
        for statement in statements:
            result = self.eval(statement)
            if type(result) == obj.Return: return result.value
            if type(result) == obj.Error: return result
        return result
    
    def eval_block_statements(self, statemenets: list[simple_ast.Statement]):
        for statement in statemenets:
            result = self.eval(statement)
            if type(result) == obj.Return or type(result) == obj.Error: return result
        return result
    
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
        return self.new_error(f'type mismatch: {left.type()} {operator} {right.type()}')
    
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
    
    def eval_if_expression(self, if_expression: simple_ast.IfExpression):
        condition = self.eval(if_expression.condition)
        if self.is_truthy(condition): return self.eval(if_expression.consequence)
        elif if_expression.alternative is not None: return self.eval(if_expression.alternative) 
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

    def is_error(self, object: obj.Object): object.type() == obj.ERROR if object is not None else False