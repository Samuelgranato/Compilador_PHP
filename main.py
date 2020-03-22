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
        if character == '/':
            return 'div'
        if character == ' ':
            return 'space'
        if character.isdigit():
            return 'int'
        if character == '(':
            return 'open_parentheses'
        if character == ')':
            return 'close_parentheses'

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

            if self.position == len(self.origin) or self.origin[self.position] == '+' or self.origin[self.position] == '-':
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

        while tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
            if tokenizer.actual.value == '+':
                tokenizer.selectNext()
                resultado += Parser.parseTerm(tokenizer)
            
            if tokenizer.actual.value == '-':
                tokenizer.selectNext()
                resultado -= Parser.parseTerm(tokenizer)
            
        return resultado

    @staticmethod
    def parseTerm(tokenizer):

        resultado = Parser.parseFactor(tokenizer)
        tokenizer.selectNext()

        while tokenizer.actual.value == '*' or tokenizer.actual.value == '/':
            if tokenizer.actual.value == '*':
                tokenizer.selectNext()
                resultado *= int(Parser.parseFactor(tokenizer))
            if tokenizer.actual.value == '/':
                tokenizer.selectNext()
                resultado //= int(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return resultado



    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            resultado = int(tokenizer.actual.value)
            return resultado
        
        elif tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '(' or tokenizer.actual.value == ')':
            if tokenizer.actual.value == '+':
                tokenizer.selectNext()
                resultado += Parser.parseFactor(tokenizer)
                
            elif tokenizer.actual.value == '-':
                tokenizer.selectNext()
                resultado -= Parser.parseFactor(tokenizer)

            elif tokenizer.actual.value == '(':
                tokenizer.selectNext()
                resultado += Parser.parseExpression(tokenizer)

                if(tokenizer.actual.value != ')'):
                    raise TypeError

            return resultado
        else:
            raise TypeError


    @staticmethod
    def run(code):
        code = Pre_proc.remove_comments(code)
        tokenizer = Tokenizer(code)
        resultado = Parser.parseExpression(tokenizer)

        if tokenizer.actual.type != 'EOF':
            raise TypeError
        return resultado

def main():
    source = sys.argv[1]
    # source = '(2*2'
    print(Parser.run(source))


if __name__== "__main__":
  main()
