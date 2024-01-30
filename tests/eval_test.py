import simple_token
import simple_parser
import simple_ast
import simple_eval
import object as obj

def test_eval_integer_expression():
    tests = [("5", 5),
            ("10", 10),
            ("-5", -5),
            ("-10", -10),
            ("5 + 5 + 5 + 5 - 10", 10),
            ("2 * 2 * 2 * 2 * 2", 32),
            ("-50 + 100 + -50", 0),
            ("5 * 2 + 10", 20),
            ("5 + 2 * 10", 25),
            ("20 + 2 * -10", 0),
            ("50 / 2 * 2 + 10", 60),
            ("2 * (5 + 10)", 30),
            ("3 * 3 * 3 + 10", 37),
            ("3 * (3 * 3) + 10", 37),
            ("(5 + 10 * 2 + 15 / 3) * 2 + -10", 50)]

    for input, expected in tests:
        evaluated = evaluate(input)
        check_integer_obj(evaluated, expected)

def test_eval_boolean_expression():
    tests = [("true", True),
            ("false", False),
            ("1 < 2", True),
            ("1 > 2", False),
            ("1 < 1", False),
            ("1 > 1", False),
            ("1 == 1", True),
            ("1 != 1", False),
            ("1 == 2", False),
            ("1 != 2", True),
            ("true == true", True),
            ("false == false", True),
            ("true == false", False),
            ("true != false", True),
            ("false != true", True),
            ("(1 < 2) == true", True),
            ("(1 < 2) == false", False),
            ("(1 > 2) == true", False),
            ("(1 > 2) == false", True),]

    for input, expected in tests:
        evaluated = evaluate(input)
        check_boolean_obj(evaluated, expected)

def test_eval_bang_operator():
    tests =  [("!true", False), ("!false", True), ("!5", False), ("!!true", True), ("!!false", False), ("!!5", True)]
    for input, expected in tests:
        evaluated = evaluate(input)
        check_boolean_obj(evaluated, expected)

def test_if_else_expressions():
    tests = [("if (true) { 10 }", 10),
        ("if (false) { 10 }", None),
        ("if (1) { 10 }", 10),
        ("if (1 < 2) { 10 }", 10),
        ("if (1 > 2) { 10 }", None),
        ("if (1 > 2) { 10 } else { 20 }", 20),
        ("if (1 < 2) { 10 } else { 20 }", 10),]

    for input, expected in tests:
        evaluated = evaluate(input)
        if expected is not None: check_integer_obj(evaluated, expected)
        else: check_null_obj(evaluated)
    
def test_return_statement():
    tests = [("return 10;", 10),
            ("return 10; 9;", 10),
            ("return 2 * 5; 9;", 10),
            ("9; return 2 * 5; 9;", 10),
            ("""if (10 > 1) {
                    if (10 > 1) {
                        return 10;
                    }
                return 1;
                }""", 10)]

    for input, expected in tests:
        evaluated = evaluate(input)
        check_integer_obj(evaluated, expected)

def test_error_handling():
    tests = [( "5 + true;", "type mismatch: INTEGER + BOOLEAN" ),
            ( "5 + true; 5;", "type mismatch: INTEGER + BOOLEAN" ),
            ( "-true", "unknown operator: -BOOLEAN" ),
            ( "true + false;", "unknown operator: BOOLEAN + BOOLEAN" ),
            ( "5; true + false; 5", "unknown operator: BOOLEAN + BOOLEAN" ),
            ( "if (10 > 1) { true + false; }", "unknown operator: BOOLEAN + BOOLEAN" ),
            ( """if (10 > 1) { if (10 > 1) { return true + false; } return 1; } """ , "unknown operator: BOOLEAN + BOOLEAN" ),
            ( "foobar", "identifier not found: foobar" )]

    for input, expected in tests:
        print(f'current test: {input}')
        evaluated = evaluate(input)
        check_error_message(evaluated, expected)

def test_let_statements():
    tests = [("let a = 5; a;", 5),
        ("let a = 5 * 5; a;", 25),
        ("let a = 5; let b = a; b;", 5),
        ("let a = 5; let b = a; let c = a + b + 5; c;", 15)]

    for input, expected in tests:
        evaluated = evaluate(input)
        check_integer_obj(evaluated, expected)

def test_function_object():
    test = "fn(x) { x + 2; };"
    evaluated = evaluate(test)
    assert type(evaluated) == obj.Function, print(f'object is not Function, got={type(evaluated)}')
    assert len(evaluated.parameters) == 1, print(f'function has wrong parameters, got={len(evaluated.parameters)}')
    assert evaluated.parameters[0].string() == "x", print(f'parameter is not \'x\', got={evaluated.parameters[0].string()}')
    assert evaluated.body.string() == "(x + 2)", print(f'body is not \'(x + 2)\', got={evaluated.body.string()}')

def test_function_application():
    tests = [("let identity = fn(x) { x; }; identity(5);", 5),
        ("let identity = fn(x) { return x; }; identity(5);", 5),
        ("let double = fn(x) { x * 2; }; double(5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5, 5);", 10),
        ("let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", 20),
        ("fn(x) { x; }(5)", 5)]
    
    for input, expected in tests:
        evaluated = evaluate(input)
        check_integer_obj(evaluated, expected)

def test_closure():
    test = """let newAdder = fn(x) {
  fn(y) { x + y };
};

let addTwo = newAdder(2);
addTwo(2);"""
    evaluated = evaluate(test)
    check_integer_obj(evaluated, 4)

def test_string_literal():
    test = '"Hello World!"'
    evaluated = evaluate(test)
    assert type(evaluated) == obj.String, print(f'object is not String, got={type(evaluated)}')
    assert evaluated.value == "Hello World!", print(f'object has wrong value, should be {test}, got={evaluated.value}')

def evaluate(input):
    lexer = simple_token.Lexer(input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    evaluator = simple_eval.Evaluator()
    environment = obj.Environment()
    return evaluator.eval(program, environment)

def check_integer_obj(object: obj.Object, expected):
    assert type(object) == obj.Integer, print(f'object is not Integer, got={type(object)}')
    assert object.value == expected, print(f'object has wrong value. should be {expected}, got={object.value}')

def check_boolean_obj(object: obj.Object, expected):
    assert type(object) == obj.Boolean, print(f'object is not Boolean, got={type(object)}')
    assert object.value == expected, print(f'object has wrong value. should be {expected}, got={object.value}')

def check_null_obj(object: obj.Object):
    assert type(object) == obj.Null, print(f'object is not Null, got={type(object)}')

def check_error_message(object: obj.Object, expected: str):
    assert type(object) == obj.Error, print(f'object is not Error, got={type(object)}')
    assert object.message ==  expected, print(f'error message does not match. expected={expected}, got={object.message}')