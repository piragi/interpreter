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
    #assert_expressions = ["5", "8", "42069"]

    for i, assert_statement in enumerate(assert_statements):
        statement = program.statements[i]
        assert statement.token_literal() == "let"
        assert statement.name.value == assert_statement
        assert statement.name.token_literal() == assert_statement

def test_return_statement():
    test_input = """return 5;
    return 10;
    return 42069;"""

    lexer = simple_token.Lexer(test_input)
    parser = simple_parser.Parser(lexer)

    program = parser.parse_program()
    check_parser_errors(parser.errors)

    assert len(program.statements) == 3

    for statement in program.statements:
        assert statement.token_literal() == "return"

def check_parser_errors(errors):
    if len(errors) is 0:
        return
    
    print(f'parser has {len(errors)} error(s).')
    for error in errors:
        print(f'parser error: {error}')
    assert False