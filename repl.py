from simple_token import Lexer, EOF


PROMPT = ">> "

class Repl():
    def scan(self):
        while True:
            repl_input = input(PROMPT)
            if repl_input == "quit" or repl_input == "q":
                return
            lexer = Lexer(repl_input)
            token = lexer.next_token()
            while token.type is not EOF:
                print(f'{token.type}: {token.literal}')
                token = lexer.next_token()

repl = Repl()
repl.scan()