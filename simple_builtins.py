import simple_eval
import object as obj

def builtin_len(args: list[obj.Object]) -> obj.Object:
    if len(args) != 1: return obj.Error(f'wrong number of arguments. got={len(args)}, want=1')
    if type(args[0]) is obj.String: return obj.Integer(len(args[0].value))
    elif type(args[0]) is obj.Array: return obj.Integer(len(args[0].elements))
    return obj.Error(f'argument to \'len\' not supported, got {args[0].type()}')

def builtin_first(args: list[obj.Object]) -> obj.Object:
    if len(args) != 1: return obj.Error(f'wrong number of arguments. got={len(args)}, want=1')
    if type(args[0]) is not obj.Array: return obj.Error(f'argument to \'first\' must be ARRAY, got {args[0].type()}')
    elif len(args[0].elements) > 0: return args[0].elements[0]
    return simple_eval.NULL

def builtin_last(args: list[obj.Object]) -> obj.Object:
    if len(args) != 1: return obj.Error(f'wrong number of arguments. got={len(args)}, want=1')
    if type(args[0]) is not obj.Array: return obj.Error(f'argument to \'last\' must be ARRAY, got {args[0].type()}')
    elif len(args[0].elements) > 0: return args[0].elements[len(args[0].elements)-1]
    return simple_eval.NULL

def builtin_rest(args: list[obj.Object]) -> obj.Object:
    if len(args) != 1: return obj.Error(f'wrong number of arguments. got={len(args)}, want=1')
    if type(args[0]) is not obj.Array: return obj.Error(f'argument to \'rest\' must be ARRAY, got {args[0].type()}')
    elif len(args[0].elements) > 0: 
        copy = []
        for element in args[0].elements[1:]: copy.append(element)
        return obj.Array(copy)
    return simple_eval.NULL

def builtin_push(args: list[obj.Object]) -> obj.Object:
    if len(args) != 2: return obj.Error(f'wrong number of arguments. got={len(args)}, want=2')
    if type(args[0]) is not obj.Array: return obj.Error(f'first argument to \'push\' must be ARRAY, got {args[0].type()}')
    if type(args[1]) is not obj.Integer: return obj.Error(f'second argument to \'push\' must be INTEGER, got {args[1].type()}')
    elif len(args[0].elements) >= 0:
        args[0].elements.append(args[1])
        return args[0]
    return simple_eval.NULL

def builtin_puts(args: list[obj.Object]) -> obj.Object:
    for arg in args:
        print(arg.inspect())
    return simple_eval.NULL

functions = {
    "len": obj.Builtin(builtin_len),
    "first": obj.Builtin(builtin_first),
    "last": obj.Builtin(builtin_last),
    "rest": obj.Builtin(builtin_rest),
    "push": obj.Builtin(builtin_push),
    "puts": obj.Builtin(builtin_puts)
    }
