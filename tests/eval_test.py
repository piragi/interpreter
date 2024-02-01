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
            ( "foobar", "identifier not found: foobar" ),
            ('"Hello" - "World"', "unknown operator: STRING - STRING",)]

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
    assert type(evaluated) == obj.Function, (f'object is not Function, got={type(evaluated)}')
    assert len(evaluated.parameters) == 1, (f'function has wrong parameters, got={len(evaluated.parameters)}')
    assert evaluated.parameters[0].string() == "x", (f'parameter is not \'x\', got={evaluated.parameters[0].string()}')
    assert evaluated.body.string() == "(x + 2)", (f'body is not \'(x + 2)\', got={evaluated.body.string()}')

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
    assert type(evaluated) == obj.String, (f'object is not String, got={type(evaluated)}')
    assert evaluated.value == "Hello World!", (f'object has wrong value, should be {test}, got={evaluated.value}')

def test_string_concatenation():
    test = '"Hello" + " " + "World!"'
    evaluated = evaluate(test)
    assert type(evaluated) == obj.String, (f'object is not String, got={type(evaluated)}')
    assert evaluated.value == "Hello World!", (f'object has wrong value, should be {test}, got={evaluated.value}')

def test_builtin():
    tests = [('len("")', 0),
            ('len("four")', 4),
            ('len("hello world")', 11),
            ('len(1)', "argument to 'len' not supported, got INTEGER"),
            ('len("one", "two")', "wrong number of arguments. got=2, want=1"),
            ('len([1, 2, 3])', 3),
		    ('len([])', 0),
		    ('puts("hello", "world!")', None),
		    ('first([1, 2, 3])', 1),
		    ('first([])', None),
		    ('first(1)', "argument to 'first' must be ARRAY, got INTEGER"),
		    ('last([1, 2, 3])', 3),
		    ('last([])', None),
		    ('last(1)', "argument to 'last' must be ARRAY, got INTEGER"),
		    ('rest([1, 2, 3])', [2,3]),
		    ('rest([])', None),
		    ('push([], 1)', [1]),
		    ('push(1, 1)', "first argument to 'push' must be ARRAY, got INTEGER")]
    
    for input, expected in tests:
        evaluated = evaluate(input)
        if type(expected) == int: check_integer_obj(evaluated, expected)
        if type(expected) == list: check_array_obj(evaluated, expected)
        if type(expected) == str: check_error_message(evaluated, expected)
        if type(expected) == None: check_null_obj(evaluated)
    
def test_array_expression():
    test = '[1, 2 * 2, 3 + 3]'
    evaluated = evaluate(test)
    assert type(evaluated) == obj.Array, (f'object is not String, got={type(evaluated)}')
    assert len(evaluated.elements) == 3, f'object has wrong number of elements. got={len(evaluated.elements)}'
    check_integer_obj(evaluated.elements[0], 1)
    check_integer_obj(evaluated.elements[1], 4)
    check_integer_obj(evaluated.elements[2], 6)

def test_array_index_expression():
    tests = [( "[1, 2, 3][0]", 1,),
            ( "[1, 2, 3][1]", 2,),
            ( "[1, 2, 3][2]", 3,),
            ( "let i = 0; [1][i];", 1,),
            ( "[1, 2, 3][1 + 1];", 3,),
            ( "let myArray = [1, 2, 3]; myArray[2];", 3,),
            ( "let myArray = [1, 2, 3]; myArray[0] + myArray[1] + myArray[2];", 6,),
            ( "let myArray = [1, 2, 3]; let i = myArray[0]; myArray[i]", 2,),
            ( "[1, 2, 3][3]", None,),
            ( "[1, 2, 3][-1]", None,)]

    for input, expected in tests:
        evaluated = evaluate(input)
        if type(expected) == int: check_integer_obj(evaluated, expected)
        if type(expected) == None: check_null_obj(evaluated)

def test_hash_literals():
    test = """let two = "two";
    {
        "one": 10 - 9,
        two: 1 + 1,
        "thr" + "ee": 6 / 2,
        4: 4,
        true: 5,
        false: 6
    }"""

    expected = {obj.String("one").hashkey(): 1,
                obj.String("two").hashkey(): 2,
                obj.String("three").hashkey(): 3,
                obj.Integer(4).hashkey(): 4,
                obj.Boolean(True).hashkey(): 5,
                obj.Boolean(False).hashkey(): 6}

    evaluated = evaluate(test)
    assert type(evaluated) == obj.Hash, f'evaluated is not of type Hash, got={type(evaluated)}'
    assert len(evaluated.dict) == len(expected), f'evaluated has not the same amount of elements, got={len(evaluated.dict)}'
    print(evaluated.inspect())
    for key, value in expected.items():
        evaluated_value = evaluated.dict.get(key)
        assert evaluated_value is not None, f'key is not inside dict'
        assert type(evaluated_value) == obj.HashPair, f'dict element is not of type HashPair, got={type(value)}'
        check_integer_obj(evaluated_value.value, value)

def test_hash_index_expressions():
    tests = [
        ( '{"foo": 5}["foo"]', 5, ),
        ( '{"foo": 5}["bar"]', None, ),
        ( 'let key = "foo"; {"foo": 5}[key]', 5, ),
        ( '{}["foo"]', None, ),
        ( '{5: 5}[5]', 5, ),
        ( '{true: 5}[true]', 5, ),
        ( '{false: 5}[false]', 5, )]

    for input, expected in tests:
        print(f'current input = {input}')
        evaluated = evaluate(input)
        if type(expected) == int: check_integer_obj(evaluated, expected)
        if type(expected) == None: check_null_obj(evaluated)

def evaluate(input):
    lexer = simple_token.Lexer(input)
    parser = simple_parser.Parser(lexer)
    program = parser.parse_program()
    evaluator = simple_eval.Evaluator()
    environment = obj.Environment()
    return evaluator.eval(program, environment)

def check_integer_obj(object: obj.Object, expected):
    assert not type(object) == obj.Error, object.message
    assert type(object) == obj.Integer, (f'object is not Integer, got={type(object)}')
    assert object.value == expected, (f'object has wrong value. should be {expected}, got={object.value}')

def check_boolean_obj(object: obj.Object, expected):
    assert not type(object) == obj.Error, object.message
    assert type(object) == obj.Boolean, (f'object is not Boolean, got={type(object)}')
    assert object.value == expected, (f'object has wrong value. should be {expected}, got={object.value}')

def check_null_obj(object: obj.Object):
    assert not type(object) == obj.Error, object.message
    assert type(object) == obj.Null, (f'object is not Null, got={type(object)}')

def check_error_message(object: obj.Object, expected: str):
    assert type(object) == obj.Error, (f'object is not Error, got={type(object)}')
    assert object.message ==  expected, (f'error message does not match. expected={expected}, got={object.message}')

def check_array_obj(object: obj.Object, expected):
    assert not type(object) == obj.Error, object.message
    assert type(object) == obj.Array, (f'object is not Array, got={type(object)}')
    assert len(object.elements) == len(expected), f'array.elements is not of same size. got={len(object.elements)}, expected={len(expected)}'
    for element, expected_element in zip(object.elements, expected):
        if type(expected_element) == obj.Integer: check_integer_obj(element, expected_element)
        if type(expected_element) == obj.Array: check_array_obj(element, expected_element)