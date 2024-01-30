import simple_eval
import object as obj

def builtin_len(args: list[obj.Object]) -> obj.Object:
    if len(args) != 1: return obj.Error(f'wrong number of arguments. got={len(args)}, want=1')
    if type(args[0]) is not obj.String: return obj.Error(f'argument to \'len\' not supported, got {args[0].type()}')
    return obj.Integer(len(args[0].value))

functions = {
    "len": obj.Builtin(builtin_len)
    }
