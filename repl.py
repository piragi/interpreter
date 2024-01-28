from simple_token import Lexer, EOF
from simple_parser import Parser


PROMPT = ">> "

class Repl():
    def scan(self):
        while True:
            repl_input = input(PROMPT)
            if repl_input == "quit" or repl_input == "q":
                return
            lexer = Lexer(repl_input)
            parser = Parser(lexer)
            program = parser.parse_program()
            if not self.check_for_errors(parser.errors): continue
            print(f'{program.string()}')

    def check_for_errors(self, errors):
        if len(errors) == 0:
            return True
    
        print(f'parser has {len(errors)} error(s).')
        for error in errors:
            print(f'parser error: {error}')

repl = Repl()
repl.scan()