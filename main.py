import sys
import copy
import re


class SymbolTable():
    
    def __init__(self):
        self.table = {}


class Node:
    def __init__(self,value):
        self.value = value
        self.children = []

    def Evaluate(symboltable):
        pass


class BinOp(Node):
    def Evaluate(self,symboltable):
        if self.value == '+':
            return self.children[0].Evaluate(symboltable) + self.children[1].Evaluate(symboltable)
        
        if self.value == '-':
            return self.children[0].Evaluate(symboltable) - self.children[1].Evaluate(symboltable)

        if self.value == '*':
            return self.children[0].Evaluate(symboltable) * self.children[1].Evaluate(symboltable)

        if self.value == '/':
            return self.children[0].Evaluate(symboltable) // self.children[1].Evaluate(symboltable)

        if self.value == 'and':
            return self.children[0].Evaluate(symboltable) and self.children[1].Evaluate(symboltable)

        if self.value == 'or':
            return self.children[0].Evaluate(symboltable) or self.children[1].Evaluate(symboltable)

        if self.value == '>':
            return self.children[0].Evaluate(symboltable) > self.children[1].Evaluate(symboltable)

        if self.value == '<':
            return self.children[0].Evaluate(symboltable) < self.children[1].Evaluate(symboltable)

        if self.value == '==':
            return self.children[0].Evaluate(symboltable) == self.children[1].Evaluate(symboltable)

class UnOp(Node):
    def Evaluate(self,symboltable):
        if self.value == '+':
            return self.children[0].Evaluate(symboltable)
        elif self.value == '-':
            return -self.children[0].Evaluate(symboltable)
        else:
            return not self.children[0].Evaluate(symboltable)

class IntVal(Node):
    def Evaluate(self,symboltable):
        return self.value

class NoOp(Node):
    def Evaluate(self,symboltable):
        pass

class Commands(Node):
    def Evaluate(self,symboltable):
        for child in self.children:
            child.Evaluate(symboltable)

class Echo(Node):
    def Evaluate(self,symboltable):
        print(self.children[0].Evaluate(symboltable))

class Assignment(Node):
    def Evaluate(self,symboltable):
        value = self.children[1].Evaluate(symboltable)
        symboltable.table[self.children[0].value] = value

class Identifier(Node):
    def Evaluate(self,symboltable):
        return symboltable.table[self.value]

class While(Node):
    def Evaluate(self,symboltable):
        while self.children[0].Evaluate(symboltable):
            self.children[1].Evaluate(symboltable)

class If(Node):
    def Evaluate(self,symboltable):
        if self.children[0].Evaluate(symboltable):
            self.children[1].Evaluate(symboltable)
        else:
            if len(self.children) == 3:
                self.children[2].Evaluate(symboltable)

class Readline(Node):
    def Evaluate(self,symboltable):
        return int(input())

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()


    def get_matches(token):
        matches = 0
        ret_type = None
        for token_type, regex in Tokenizer.get_tokens_regex().items():
            pattern = re.compile(regex[0]) if regex[1] == None else re.compile(regex[0], flags = regex[1])
            if pattern.match(token):
                matches += 1
                ret_type = token_type
        return matches,ret_type


    def get_tokens_regex():
        tokens_regex = {}

        tokens_regex['plus']              = ('^[+]$',None)
        tokens_regex['minus']             = ('^[-]$',None)
        tokens_regex['mult']              = ('^[*]$',None)
        tokens_regex['div']               = ('^[/]$',None)
        tokens_regex['space']             = ('^[ ]+$' ,None)
        tokens_regex['int']               = ('^[0-9]+$',None)
        tokens_regex['open_parentheses']  = ('^[(]$',None)
        tokens_regex['close_parentheses'] = ('^[)]$',None)
        tokens_regex['open_block']        = ('^[{]$',None)
        tokens_regex['close_block']       = ('^[}]$',None)
        tokens_regex['assignment']        = ('^[=]$',None)
        tokens_regex['semi-collon']       = ('^[;]$',None)
        tokens_regex['echo']              = ('^echo$',re.IGNORECASE)
        tokens_regex['identifier']        = ('^[$][a-zA-Z][a-zA-Z0-9_]*$',None)
        tokens_regex['while']        = ('^while$',None)
        tokens_regex['if']        = ('^if$',None)
        tokens_regex['else']        = ('^else$',None)
        tokens_regex['and']        = ('^and$',None)
        tokens_regex['or']        = ('^or$',None)
        tokens_regex['not']        = ('^!$',None)
        tokens_regex['equals']        = ('^==$',None)
        tokens_regex['notequals']        = ('^!=$',None)
        tokens_regex['greater']        = ('^>$',None)
        tokens_regex['less']        = ('^<$',None)
        tokens_regex['readline']        = ('^readline\(\)$',None)

        return tokens_regex



    def selectNext(self):
        if self.position == len(self.origin):
            next_token = Token('EOF')
            self.actual = next_token
            return

        token_value = self.origin[self.position]
        while token_value == '\n' and self.position + 1  != len(self.origin):
            self.position += 1
            token_value = self.origin[self.position]
        matches, token_type = Tokenizer.get_matches(token_value)
        
        while matches != 1:
            self.position += 1
            token_value += self.origin[self.position]
            matches, token_type = Tokenizer.get_matches(token_value)

        token_value_aux = token_value

        while matches != 0 and self.position + 1  != len(self.origin):
            token_value = token_value_aux
            self.position += 1
            token_value_aux += self.origin[self.position]
            matches, token_type_dummy = Tokenizer.get_matches(token_value_aux)

        if token_value.endswith('\n'):
            token_value = token_value.replace('\n','')

        if ' ' in token_value:
            self.selectNext()
            return
        
        self.actual = Token(token_type)
        self.actual.value = token_value

        

class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/",re.DOTALL) ,"" ,code)
        return code

class Parser:
    @staticmethod
    def parseBlock(tokenizer):
        node_root = Node(None)
        block_root = Commands(node_root)

        if tokenizer.actual.value == '{':
            tokenizer.selectNext()

            while tokenizer.actual.value != '}':
                command = Parser.parseCommand(tokenizer)
                if command != None:
                    block_root.children.append(command)
                tokenizer.selectNext()

        else:
            raise TypeError

        return block_root


    @staticmethod
    def parseCommand(tokenizer):
        if tokenizer.actual.type == 'identifier':
            command = Assignment(None)
            identifier = Identifier(tokenizer.actual.value)
            command.children.append(identifier)
            tokenizer.selectNext()

            if tokenizer.actual.value == '=':
                tokenizer.selectNext()
                
                command.children.append(Parser.parseRelexpr(tokenizer))
                return command


        elif tokenizer.actual.value.lower() == 'echo':
            command = Echo(tokenizer.actual.value)
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))
            
            if tokenizer.actual.value != ';':
                raise TypeError
            return command


        elif tokenizer.actual.type == 'while':
            command = While(tokenizer.actual.value)
            tokenizer.selectNext()

            if tokenizer.actual.value != '(':
                raise TypeError
            tokenizer.selectNext()

            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.value != ')':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.value == '{':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.value != '}':
                    raise TypeError
            else:
                command.children.append(Parser.parseBlock(tokenizer))


            return command
            
        elif tokenizer.actual.type == 'if':
            command = If(tokenizer.actual.value)
            tokenizer.selectNext()

            if tokenizer.actual.value != '(':
                raise TypeError
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.value != ')':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.value == '{':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.value != '}':
                    raise TypeError
            else:
                command.children.append(Parser.parseCommand(tokenizer))

            tokenizer_next = copy.copy(tokenizer)
            tokenizer_next.selectNext()
            if tokenizer_next.actual.value == 'else':
                tokenizer.selectNext()
                tokenizer.selectNext()
                if tokenizer.actual.value == '{':
                    command.children.append(Parser.parseBlock(tokenizer))
                    if tokenizer.actual.value != '}':
                        raise TypeError
                else:
                    command.children.append(Parser.parseCommand(tokenizer))
            

            return command
            
        elif tokenizer.actual.value == ';':
            pass

        else:
            command = Parser.parseBlock(tokenizer)
            return command

    @staticmethod
    def parseRelexpr(tokenizer):
        node = Parser.parseExpression(tokenizer)
        relexpr_root = node

        
        while tokenizer.actual.value == '==' or tokenizer.actual.value == '>' or tokenizer.actual.value == '<' or tokenizer.actual.value == '!=':
            if len(relexpr_root.children) == 2:
                relexpr_root_aux = BinOp(tokenizer.actual.value)
                relexpr_root_aux.children.append(relexpr_root)
                tokenizer.selectNext()
                relexpr_root_aux.children.append(Parser.parseFactor(tokenizer))
                relexpr_root = relexpr_root_aux
            else:
                relexpr_root = BinOp(tokenizer.actual.value)
                relexpr_root.children.append(node)
                tokenizer.selectNext()
                relexpr_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return relexpr_root
        
    @staticmethod
    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        root = node

        while tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == 'or':
                if len(root.children) == 2:
                    root_aux = BinOp(tokenizer.actual.value)
                    root_aux.children.append(root)
                    tokenizer.selectNext()
                    root_aux.children.append(Parser.parseTerm(tokenizer))
                    root = root_aux
                else:
                    root = BinOp(tokenizer.actual.value)
                    root.children.append(node)
                    tokenizer.selectNext()
                    root.children.append(Parser.parseTerm(tokenizer))           
        return root

    @staticmethod
    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        term_root = node
        tokenizer.selectNext()

        
        while tokenizer.actual.value == '*' or tokenizer.actual.value == '/' or tokenizer.actual.value == 'and':
            if len(term_root.children) == 2:
                term_root_aux = BinOp(tokenizer.actual.value)
                term_root_aux.children.append(term_root)
                tokenizer.selectNext()
                term_root_aux.children.append(Parser.parseFactor(tokenizer))
                term_root = term_root_aux
            else:
                term_root = BinOp(tokenizer.actual.value)
                term_root.children.append(node)
                tokenizer.selectNext()
                term_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return term_root

    @staticmethod
    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            factor_root = IntVal(int(tokenizer.actual.value))
            return factor_root
        
        elif tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '!' or tokenizer.actual.value == '(' or tokenizer.actual.value == ')' or tokenizer.actual.type == 'identifier' or tokenizer.actual.type == 'readline':
            if tokenizer.actual.value == '+' or tokenizer.actual.value == '-' or tokenizer.actual.value == '!':
                factor_root = UnOp(tokenizer.actual.value)
                tokenizer.selectNext()
                factor_root.children.append(Parser.parseFactor(tokenizer))

        
            elif tokenizer.actual.value == '(':
                tokenizer.selectNext()
                factor_root = Parser.parseRelexpr(tokenizer)

                if(tokenizer.actual.value != ')'):
                    raise TypeError

            elif tokenizer.actual.type == 'identifier':
                factor_root = Identifier(tokenizer.actual.value)

            elif tokenizer.actual.type == 'readline':
                factor_root = Readline(tokenizer.actual.value)

            return factor_root
        else:
            raise TypeError

    @staticmethod
    def run(source):
        sourcefile = open(source, 'r') 
        lines = sourcefile.read() 
        sourcefile.close()

        lines = Pre_proc.remove_comments(lines)
        tokenizer = Tokenizer(lines)
        ast = Parser.parseBlock(tokenizer)
        symboltable = SymbolTable()
        ast.Evaluate(symboltable)
        

def main():
    source = sys.argv[1]
    Parser.run(source)


if __name__== "__main__":
  main()
