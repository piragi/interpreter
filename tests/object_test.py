import simple_token
import simple_parser
import simple_ast
import object

def test_string_hashes():
    string_1 = object.String("hello world!")
    string_2 = object.String("hello world!")
    boolean_1 = object.Boolean(True)
    boolean_2 = object.Boolean(True)
    integer_1 = object.Integer(420)
    integer_2 = object.Integer(420)

    integer_3 = object.Integer(1)
    boolean_3 = object.Boolean(True)
    string_3 = object.String("1")
    
    assert string_1.hashkey() == string_2.hashkey(), f'hashkeys of String are not equal'
    assert boolean_1.hashkey() == boolean_2.hashkey(), f'hashkeys of Boolean are not equal'
    assert integer_1.hashkey() == integer_2.hashkey(), f'hashkeys of Integer are not equal'
    assert integer_3.hashkey() != boolean_3.hashkey(), f'hashkeys of different value are equal'
    assert integer_3.hashkey() != string_3.hashkey(), f'hashkeys of different value are equal'
    assert boolean_3.hashkey() != string_3.hashkey(), f'hashkeys of different value are equal'
    