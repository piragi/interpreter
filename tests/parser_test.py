import simple_token
import simple_parser
import simple_ast

def test_let_statements():
    test_input = """let x = 5;
    let y = 8;
    let foobar = 42069;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser.errors)

    assert len(program.statements) == 3

    assert_statements = ["x", "y", "foobar"]
    assert_expressions = [5, 8, 42069]

    for i, assert_statement in enumerate(assert_statements):
        statement = program.statements[i]
        assert statement.token_literal() == "let"
        assert statement.name.value == assert_statement
        assert statement.name.token_literal() == assert_statement
        assert statement.value.value == assert_expressions[i]

def test_return_statement():
    test_input = """return 5;
    return 10;
    return 42069;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser.errors)

    assert len(program.statements) == 3

    assert_expressions = [5, 10, 42069]
    for i, statement in enumerate(program.statements):
        assert statement.token_literal() == "return"
        assert statement.value.value == assert_expressions[i]
    
def test_identifier_expression():
    test_input = """foobar;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser.errors)

    statement = program.statements[0]
    assert len(program.statements) == 1
    assert type(statement) == simple_ast.ExpressionStatement
    assert type(statement.expression) == simple_ast.Identifier
    assert statement.expression.value == "foobar"
    assert statement.expression.token_literal() == "foobar"

def test_identifier_expression():
    test_input = """5;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser.errors)

    statement = program.statements[0]
    assert len(program.statements) == 1
    assert type(statement) == simple_ast.ExpressionStatement
    assert type(statement.expression) == simple_ast.IntegerLiteral
    assert statement.expression.value == 5
    assert statement.expression.token_literal() == "5"

def test_boolean():
    test_data = [("true", True), ("true;", True), ("false", False), ("false;", False)]

    for (input, expected) in test_data:
        lexer = simple_token.Lexer(input)
        parser = simple_parser.Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser.errors)

        statement = program.statements[0]
        assert len(program.statements) == 1
        assert type(statement) == simple_ast.ExpressionStatement
        assert type(statement.expression) == simple_ast.Boolean
        assert statement.expression.value == expected

def test_prefix_expression():
    test_input = ["!5;","-15;"]
    test_expected = [["!", 5], ["-", 15]]

    for input, expected in zip(test_input, test_expected):
        lexer = simple_token.Lexer(input)
        parser = simple_parser.Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser.errors)

        statement = program.statements[0]
        assert len(program.statements) == 1
        assert type(statement) == simple_ast.ExpressionStatement
        assert type(statement.expression) == simple_ast.PrefixExpression
        assert statement.expression.operator == expected[0]
        assert integer_literal(statement.expression.right, expected[1])
    
def test_infix_expression():
    test_data = [(["5 + 5"],[5, "+", 5]), (["5 - 5"],[5, "-", 5]), (["5 * 5"],[5, "*", 5]), (["5 / 5"],[5, "/", 5]), (["5 > 5"],[5, ">", 5]), (["5 < 5"],[5, "<", 5]), (["5 == 5"],[5, "==", 5]), (["5 != 5"],[5, "!=", 5]), 
                 (["ident - ident"], ["ident", "-", "ident"]), (["ident - ident"],["ident", "-", "ident"]), (["ident * ident"],["ident", "*", "ident"]), (["ident / ident"],["ident", "/", "ident"]), 
                (["ident > ident"],["ident", ">", "ident"]), (["ident < ident"],["ident", "<", "ident"]), (["ident == ident"],["ident", "==", "ident"]), (["ident != ident"],["ident", "!=", "ident"]),
                (["true == true"],[True, "==", True]), (["true != false"], [True, "!=", False]), (["false == false"], [False, "==", False])]
    for input, expected in test_data:
        lexer = simple_token.Lexer(input[0])
        parser = simple_parser.Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser.errors)

        statement = program.statements[0]
        assert len(program.statements) == 1
        assert type(statement) == simple_ast.ExpressionStatement
        assert type(statement.expression) == simple_ast.InfixExpression
        assert infix_expression(statement.expression, expected[0], expected[1], expected[2])
    
def test_operator_precedence():
    test_input = [
    "-a * b",
    "!-a",
    "a + b + c",
    "a + b - c",
    "a * b * c",
    "a * b / c",
    "a + b / c",
    "a + b * c + d / e - f",
    "3 + 4; -5 * 5",
    "5 > 4 == 3 < 4",
    "5 < 4 != 3 > 4",
    "3 + 4 * 5 == 3 * 1 + 4 * 5",
    "true",
    "false",
    "3 > 5 == false",
    "3 < 5 == true",
    "1 + (2 + 3) + 4",
    "(5 + 5) * 2",
    "2 / (5 + 5)",
    "-(5 + 5)",
    "!(true == true)",
    "a * [1, 2, 3, 4][b * c] * d",
    "add(a * b[2], b[1], 2 * [1, 2][1])"]

    test_expected = [
    "((-a) * b)",
    "(!(-a))",
    "((a + b) + c)",
    "((a + b) - c)",
    "((a * b) * c)",
    "((a * b) / c)",
    "(a + (b / c))",
    "(((a + (b * c)) + (d / e)) - f)",
    "(3 + 4)((-5) * 5)",
    "((5 > 4) == (3 < 4))",
    "((5 < 4) != (3 > 4))",
    "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))",
    "true",
    "false",
    "((3 > 5) == false)",
    "((3 < 5) == true)",
    "((1 + (2 + 3)) + 4)",
    "((5 + 5) * 2)",
    "(2 / (5 + 5))",
    "(-(5 + 5))",
    "(!(true == true))",
    "((a * ([1, 2, 3, 4][(b * c)])) * d)",
    "add((a * (b[2])), (b[1]), (2 * ([1, 2][1])))"]

    for input, expected in zip(test_input, test_expected):
        lexer = simple_token.Lexer(input)
        parser = simple_parser.Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser.errors)
        assert program.string() == expected

def test_if():
    test_input = 'if (x < y) { x }'
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.IfExpression, f'statement.expression is not IfExpression, got={type(statement.expression)}'
    assert infix_expression(statement.expression.condition, "x", "<", "y"), f'condition does not match, got={statement.expression.condition.string()}'
    assert len(statement.expression.consequence.statements) == 1, f'consequence.statements does not contain 1 statements, got={len(statement.expression.consequence.statements)}'
    consequence_statement = statement.expression.consequence.statements[0]
    assert type(consequence_statement) == simple_ast.ExpressionStatement, f'consequence statement is not ExpressionStatement, got={type(consequence_statement)}'
    assert identifier(consequence_statement.expression, "x"), f'consequence does not match, got={consequence_statement.string()}'

def test_if_else():
    test_input = 'if (x < y) { x } else { y }'
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.IfExpression, f'statement.expression is not IfExpression, got={type(statement.expression)}'
    assert infix_expression(statement.expression.condition, "x", "<", "y"), f'condition does not match, got={statement.expression.condition.string()}'
    assert len(statement.expression.consequence.statements) == 1, f'consequence.statements does not contain 1 statements, got={len(statement.expression.consequence.statements)}'
    consequence_statement = statement.expression.consequence.statements[0]
    assert type(consequence_statement) == simple_ast.ExpressionStatement, f'consequence statement is not ExpressionStatement, got={type(consequence_statement)}'
    assert identifier(consequence_statement.expression, "x"), f'consequence does not match, got={statement.expression.condition.string()}'
    alternative_statement = statement.expression.alternative.statements[0]
    assert type(alternative_statement) == simple_ast.ExpressionStatement, f'alternative statement is not ExpressionStatement, got={type(alternative_statement)}'
    assert identifier(alternative_statement.expression, "y"), f'alternative does not match, got={alternative_statement.string()}'

def test_functions():
    test_input = ['fn (x, y) { x + y; }', 'fn () { x + y; }', 'fn (x, y, z) { x + y; }']
    expected_params = [['x', 'y'], [], ['x', 'y', 'z']]

    for input, param in zip(test_input, expected_params):
        function_with_params(input, param)

def test_call_expression():
    test_input = 'add(1, 2 * 3, 4 + 5);'
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.CallExpression, f'statement.expression is not CallExpression, got={type(statement.expression)}'
    assert identifier(statement.expression.function, "add"), f'callable identifier does not match. should be add, got={statement.expression.function.string()}'
    assert len(statement.expression.arguments) == 3; f'callable parameters are wrong. should be 3, got={len(statement.expression.arguments)}'
    assert literal_expression(statement.expression.arguments[0], 1)
    assert infix_expression(statement.expression.arguments[1], 2, "*", 3)
    assert infix_expression(statement.expression.arguments[2], 4, "+", 5)

def test_string_literals():
    test_input = '"hello world"'
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.StringLiteral, f'statement.expression is not StringLiteral, got={type(statement.expression)}'
    assert statement.expression.value == "hello world", f'literal.value is not {test_input}, got={statement.expression.value}'

def test_array_literals():
    test_input = "[1, 2 * 2, 3 + 3]"

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.ArrayLiteral, f'statement.expression is not ArrayLiteral, got={type(statement.expression)}'
    assert len(statement.expression.elements) == 3, f'array.elements does not contain 3 elements, got={len(statement.expression.elements)}'
    assert integer_literal(statement.expression.elements[0], 1), f'integer does not match, got={statement.expression.elements[0].value}'
    assert infix_expression(statement.expression.elements[1], 2, "*", 2), f'infix does not match, got={statement.expression.elements[1].left} {statement.expression.elements[1].operator} {statement.expression.elements[1].right}'
    assert infix_expression(statement.expression.elements[2], 3, "+", 3), f'infix does not match, got={statement.expression.elements[2].left} {statement.expression.elements[2].operator} {statement.expression.elements[2].right}'

def test_array_literal_empty():
    test_input = "[]"

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.ArrayLiteral, f'statement.expression is not ArrayLiteral, got={type(statement.expression)}'
    assert len(statement.expression.elements) == 0, f'array.elements does not contain 0 elements, got={len(statement.expression.elements)}'

def test_index_expression():
    test_input = "myArray[1 + 1]"

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.IndexExpression, f'statement.expression is not IndexExpression, got={type(statement.expression)}'
    assert identifier(statement.expression.left, "myArray"), f'index_element.left does not match, got={statement.expression.left}'
    assert infix_expression(statement.expression.index, 1, "+", 1), f'index_element.left does not match, got={statement.expression.left.string()}'

def test_hash_literal_string_keys():
    test_input = '{"one": 1, "two": 2, "three": 3}'
    expected_dictionary = {"one": 1, "two": 2, "three": 3}

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.HashLiteral, f'statement.expression is not HashLiteral, got={type(statement.expression)}'
    dictionary = statement.expression.dict
    assert len(dictionary) == 3, f'dictionary length does not match, got={len(dictionary)}'
    for (key, value), (expected_key, expected_value) in zip(dictionary.items(), expected_dictionary.items()):
        assert type(key) == simple_ast.StringLiteral, f'dictionary.key is not StringLiteral, got={type(key)}'
        assert expected_dictionary[key.value] == expected_value, f'dictionary.key not as expected, got={key}'
        assert integer_literal(dictionary[key], expected_value)

def test_hash_literal_integer_keys():
    test_input = '{1: 1, 2: 2, 3: 3}'
    expected_dictionary = {1: 1, 2: 2, 3: 3}

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.HashLiteral, f'statement.expression is not HashLiteral, got={type(statement.expression)}'
    dictionary = statement.expression.dict
    assert len(dictionary) == 3, f'dictionary length does not match, got={len(dictionary)}'
    for (key, value), (expected_key, expected_value) in zip(dictionary.items(), expected_dictionary.items()):
        assert type(key) == simple_ast.IntegerLiteral, f'dictionary.key is not IntegerLiteral, got={type(key)}'
        assert expected_dictionary[key.value] == expected_value, f'dictionary.key not as expected, got={key}'
        assert integer_literal(dictionary[key], expected_value)

def test_hash_literal_boolean_keys():
    test_input = '{"true": 1, "false": 2}'
    expected_dictionary = {True: 1, False: 2}

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.HashLiteral, f'statement.expression is not HashLiteral, got={type(statement.expression)}'
    dictionary = statement.expression.dict
    assert len(dictionary) == 3, f'dictionary length does not match, got={len(dictionary)}'
    for (key, value), (expected_key, expected_value) in zip(dictionary.items(), expected_dictionary.items()):
        assert type(key) == simple_ast.Boolean, f'dictionary.key is not Boolean, got={type(key)}'
        assert expected_dictionary[key.value] == expected_value, f'dictionary.key not as expected, got={key}'
        assert integer_literal(dictionary[key], expected_value)

    
def test_hash_literal_boolean_keys():
    test_input = '{"one": 0 + 1, "two": 10 - 8, "three": 15 / 5}'
    expected_dictionary = {"one": lambda e: infix_expression(e, 0, "+", 1),
                           "two": lambda e: infix_expression(e, 10, "-", 8), 
                           "three": lambda e: infix_expression(e, 15, "/", 5)}

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.HashLiteral, f'statement.expression is not HashLiteral, got={type(statement.expression)}'
    dictionary = statement.expression.dict
    assert len(dictionary) == 3, f'dictionary length does not match, got={len(dictionary)}'
    for key, value in dictionary.items():
        assert type(key) == simple_ast.StringLiteral, f'dictionary.key is not StringLiteral, got={type(key)}'
        test = expected_dictionary.get(key.value)
        assert test is not None, f'dictionary.key not as expected, got={key}'
        assert test(value)

def test_empty_hash_literal():
    test_input = '{}'
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.HashLiteral, f'statement.expression is not HashLiteral, got={type(statement.expression)}'
    assert len(statement.expression.dict) == 0, f'dictionary length does not match, got={len(statement.expression.dict)}'

def function_with_params(test_input, parameters):
    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    statement = program.statements[0]
    check_parser_errors(parser.errors)

    assert len(program.statements) == 1, f'program.statements does not contain 1 statements, got={len(program.statments)}'
    assert type(statement) == simple_ast.ExpressionStatement, f'program.statements[0] is not ExpressionStatement, got={type(statement)}'
    assert type(statement.expression) == simple_ast.FunctionLiteral, f'statement.expression is not FunctionLiteral, got={type(statement.expression)}'
    assert len(statement.expression.parameters) == len(parameters), f'function literal parameters wrong. should be {len(parameters)}, got={len(statement.expression.parameters)}'
    for i, parameter in enumerate(parameters):
        assert identifier(statement.expression.parameters[i], parameter), f'parameter identifier wrong. should be {parameter}, got={statement.expression.parameters[i]}'
    assert len(statement.expression.body.statements) == 1, f'function literal body wrong. should be 1, got={len(statement.expression.body)}'
    assert type(statement.expression.body) == simple_ast.BlockStatement, f'body is not BlockStatement, got={type(statement.expression.body)}'
    assert infix_expression(statement.expression.body.statements[0].expression, "x", "+", "y"), f'function literal body expression wrong. should be "(x + y)" , got={statement.expression.body.statements[0].string()}'

def integer_literal(integer_literal: simple_ast.Expression, value: int):
    if type(integer_literal) is not simple_ast.IntegerLiteral: 
        return False
    if integer_literal.value != value:
        return False
    if integer_literal.token_literal() != str(value):
        return False
    return True

def identifier(expression: simple_ast.Expression, value: str):
    if type(expression) is not simple_ast.Identifier:
        return False
    if expression.value != value:
        return False
    if expression.token_literal() != value:
        return False
    return True
    
def literal_expression(expression: simple_ast.Expression, expected):
    if type(expected) is int:
        return integer_literal(expression, expected)
    if type(expected) is str:
        return identifier(expression, expected)
    if type(expected) is bool:
        return boolean(expression, expected)
    print(f'type of {type(expected)} cannot be handled')
    return False

def boolean(boolean: simple_ast.Expression, value):
    print(f'boolean.value = {boolean.value}, value = {value}')
    if type(boolean) is not simple_ast.Boolean:
        return False
    if boolean.value != value:
        return False
    # TODO: check token_literal() needs true, not True
    return True

def infix_expression(expression: simple_ast.Expression, left, operator, right):
    if type(expression) is not simple_ast.InfixExpression:
        print(f'expression is of type {type(expression)}, should be InfixExpression')
        return False
    if not literal_expression(expression.left, left):
        print(f'expression.left has value {expression.left.string()}, should be {left}.')
        return False
    if expression.operator != operator:
        print(f'expression has operator {expression.operator}, should be {operator}') 
        return False
    if not literal_expression(expression.right, right):
        print(f'expression.left has value {expression.right.string()}, should be {right}')
        return False
    return True 

def check_parser_errors(errors):
    if len(errors) == 0:
        return
    
    print(f'parser has {len(errors)} error(s).')
    for error in errors:
        print(f'parser error: {error}')
    assert False