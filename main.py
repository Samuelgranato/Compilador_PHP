import sys
import copy
import re

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()

    def get_type(character):
        if character == '+':
            return 'plus'
        if character == '-':
            return 'minus'
        if character == '*':
            return 'mult'
        if character == '-/':
            return 'div'
        if character == ' ':
            return 'space'
        if character.isdigit():
            return 'int'

    def selectNext(self):
        if self.position == len(self.origin):
            next_token = Token('EOF')
            self.actual = next_token
            return

        current_char = self.origin[self.position]
        while(current_char == ' '):
            self.position += 1
            if self.position == len(self.origin):
                next_token = Token('EOF')
                self.actual = next_token
                return

            current_char = self.origin[self.position]
            
        next_token = Token(Tokenizer.get_type(current_char))
        while Tokenizer.get_type(current_char) == next_token.type:
            next_token.value += self.origin[self.position]
            self.position += 1

            if self.position == len(self.origin):
                self.actual = next_token
                return

            current_char = self.origin[self.position]

        self.actual = next_token


class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL) ,"" ,code)
        return code


class Parser:
    @staticmethod
    def parseExpression(tokenizer):
        resultado = Parser.parseTerm(tokenizer)
        tokenizer.selectNext()

        while tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
            if tokenizer.actual.value == '+':
                tokenizer.selectNext()
                resultado += Parser.parseTerm(tokenizer)
            
            if tokenizer.actual.value == '-':
                tokenizer.selectNext()
                resultado -= Parser.parseTerm(tokenizer)
            
            tokenizer.selectNext()

        if(tokenizer.actual.type != 'EOF'):
            raise TypeError
        return resultado
    @staticmethod
    def parseTerm(tokenizer):
        tokenizer_next = copy.copy(tokenizer)

        if tokenizer.actual.type == 'int':
            resultado = int(tokenizer.actual.value)
            tokenizer_next.selectNext()

            while tokenizer_next.actual.value == '*' or tokenizer_next.actual.value == '/':
                if tokenizer_next.actual.value == '*':
                    tokenizer_next.selectNext()
                    tokenizer.selectNext()
                    if tokenizer_next.actual.type == 'int':
                        resultado *= int(tokenizer_next.actual.value)
                    else:
                        raise TypeError
                if tokenizer_next.actual.value == '/':
                    tokenizer_next.selectNext()
                    tokenizer.selectNext()
                    if tokenizer_next.actual.type == 'int':
                        resultado //= int(tokenizer_next.actual.value)
                    else:
                        raise TypeError
                tokenizer_next.selectNext()
                tokenizer.selectNext()

            return resultado
        else:
            raise TypeError


    @staticmethod
    def run(code):
        code = Pre_proc.remove_comments(code)
        # print(code)
        tokenizer = Tokenizer(code)
        return Parser.parseExpression(tokenizer)

def main():
    source = sys.argv[1]
    # source = '1+2*3+2+2*2*2'
    print(Parser.run(source))


if __name__== "__main__":
  main()
