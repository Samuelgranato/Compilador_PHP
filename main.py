import sys
import copy
import re
import operator


class SymbolTable():
    
    def __init__(self):
        self.table = {}
        self.functions = {}

    def set_symboltable(self,symboltable):
        self.table = symboltable.table


class Node:
    def __init__(self,value,node_type):
        self.value = value
        self.children = []
        self.type = node_type

    def Evaluate(symboltable):
        pass


class BinOp(Node):
    def Evaluate(self,symboltable):
        child0_value = self.children[0].Evaluate(symboltable)
        child1_value = self.children[1].Evaluate(symboltable)

        if self.type == 'concat':
            return str(child0_value) + str(child1_value)

        if self.type == 'equals':
            return child0_value == child1_value

        if self.children[0].type == 'string' or self.children[1].type == 'string':
            raise TypeError

        if self.type == 'plus': 
            return child0_value + child1_value
        
        if self.type == 'minus':
            return child0_value - child1_value

        if self.type == 'mult':
            return child0_value * child1_value

        if self.type == 'div':
            return child0_value // child1_value

        if self.type == 'and':
            return child0_value and child1_value

        if self.type == 'or':
            return child0_value or child1_value

        if self.type == 'greater':
            return child0_value > child1_value

        if self.type == 'less':
            return child0_value < child1_value




            
class UnOp(Node):
    def Evaluate(self,symboltable):
        if self.type == 'plus':
            return self.children[0].Evaluate(symboltable)
        elif self.type == 'minus':
            return -self.children[0].Evaluate(symboltable)
        else:
            return not self.children[0].Evaluate(symboltable)

class IntVal(Node):
    def Evaluate(self,symboltable):
        return self.value
    
class BoolVal(Node):
    def Evaluate(self,symboltable):
        return self.value

class StringVal(Node):
    def Evaluate(self,symboltable):
        return self.value

class NoOp(Node):
    def Evaluate(self,symboltable):
        pass

class Commands(Node):
    def Evaluate(self,symboltable):
        for child in self.children:
            ret_val = child.Evaluate(symboltable)
            if ret_val is not None:
                return ret_val

class Program(Node):
    def Evaluate(self,symboltable):
       self.children[0].Evaluate(symboltable)

class Echo(Node):
    def Evaluate(self,symboltable):
        print(self.children[0].Evaluate(symboltable))

class Assignment(Node):
    def Evaluate(self,symboltable):
        value = self.children[1].Evaluate(symboltable)
        symboltable.table[self.children[0].value] = (value, self.children[1].type)

class Identifier(Node):
    def Evaluate(self,symboltable):
        self.type = symboltable.table[self.value][1] 
        return symboltable.table[self.value][0]

class While(Node):
    def Evaluate(self,symboltable):
        ret_val = None
        while self.children[0].Evaluate(symboltable) and ret_val is None:
            ret_val = self.children[1].Evaluate(symboltable)
        return ret_val

class If(Node):
    def Evaluate(self,symboltable):
        if self.children[0].Evaluate(symboltable):
            return self.children[1].Evaluate(symboltable)
        else:
            if len(self.children) == 3:
                return self.children[2].Evaluate(symboltable)

class Readline(Node):
    def Evaluate(self,symboltable):
        return int(input())

class FuncDec(Node):
    def Evaluate(self,symboltable):
        if self.value in symboltable.functions:
            raise TypeError
        symboltable.functions[self.value] = self

class FuncCall(Node):
    def Evaluate(self,symboltable):
        calling_func_table = copy.copy(symboltable)
        symboltable.table = {}
        calling_func = symboltable.functions[self.value]
        for i in range(len(calling_func.children) - 1):
            arg = calling_func.children[i]
            eval_value = self.children[i].Evaluate(calling_func_table)
            symboltable.table[arg.value] = (eval_value, self.children[i].type)

        ret_val = calling_func.children[len(calling_func.children)-1].Evaluate(symboltable)
        symboltable.set_symboltable(calling_func_table)
        return ret_val

class Return(Node):
    def Evaluate(self,symboltable):
        return self.children[0].Evaluate(symboltable)

class Token:
    def __init__(self,token_type):
        self.type = token_type
        self.value = ''

class Tokenizer:
    def __init__(self,origin):
        self.origin = origin
        self.position = 0
        self.selectNext()


    def get_matches(token, tokens_dict):
        matches = 0
        ret_type = None
        for token_type, regex in tokens_dict.items():
            pattern = re.compile(regex[0]) if regex[1] == None else re.compile(regex[0], flags = regex[1])
            if pattern.match(token.lower()):
                matches += 1
                ret_type = token_type
        return matches,ret_type

    def get_tokens_reserved():
        tokens_reserved = {}

        tokens_reserved['readline']        = ('readline\(\)$', None)
        tokens_reserved['open_program']    = ('<\?php$', None)
        tokens_reserved['close_program']   = ('\?>$', None)
        tokens_reserved['while']           = ('while *\($', None)
        tokens_reserved['if']              = ('if *\($', None)
        tokens_reserved['else']            = ('else *{$', None)
        tokens_reserved['and']             = ('and $', None)
        tokens_reserved['or']              = ('or $', None)
        tokens_reserved['equals']          = ('\=\=$', None)
        tokens_reserved['echo']            = ('echo $', None)
        tokens_reserved['readline']        = ('readline\(\)$', None)
        tokens_reserved['true']            = ('true$', None)
        tokens_reserved['false']           = ('false$', None)
        tokens_reserved['funcdec']         = ('function $', None)
        tokens_reserved['return']          = ('return $', None)

        return tokens_reserved



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
        tokens_regex['identifier']        = ('^[$][a-zA-Z][a-zA-Z0-9_]*$',None)
        tokens_regex['string']            = ('^\".*\"$',None)
        tokens_regex['not']               = ('^!$',None)
        tokens_regex['notequals']         = ('^!=$',None)
        tokens_regex['greater']           = ('^>$',None)
        tokens_regex['less']              = ('^<$',None)
        tokens_regex['concat']            = ('^\.$',None)
        tokens_regex['comma']             = ('^\,$',None)
        tokens_regex['function']          = ('^[a-zA-Z][a-zA-Z0-9_]*$',None)


        return tokens_regex


    def get_token_value(self,tokens_dict):
        token_value = self.origin[self.position]

        token_value = self.origin[self.position]
        while token_value == '\n' and self.position + 1  != len(self.origin):
            self.position += 1
            token_value = self.origin[self.position]
        matches, token_type = Tokenizer.get_matches(token_value, tokens_dict)
        
        while matches != 1 and self.position + 1  != len(self.origin):
            self.position += 1
            token_value += self.origin[self.position]
            matches, token_type = Tokenizer.get_matches(token_value, tokens_dict)

        token_value_aux = token_value

        while matches != 0 and self.position + 1  != len(self.origin):
            token_value = token_value_aux
            self.position += 1
            token_value_aux += self.origin[self.position]
            matches, token_type_dummy = Tokenizer.get_matches(token_value_aux, tokens_dict)

        if token_type == None:
            return

        return token_value, token_type

    def get_token_reserved_value(self):
        reserved_tokens = Tokenizer.get_tokens_reserved()

        for token_type, value in reserved_tokens.items():
            word = self.origin[self.position: self.position + len(value)]
            if word.lower() == value:
                self.position += len(value)
                return value, token_type

        return

    def selectNext(self):
        if self.position == len(self.origin):
            next_token = Token('EOF')
            self.actual = next_token
            return

        while self.origin[self.position] == '\n' or self.origin[self.position] == ' ':
            self.position += 1
            
            if self.position == len(self.origin):
                next_token = Token('EOF')
                self.actual = next_token
                return

        position_aux = self.position
        token_return = self.get_token_value(Tokenizer.get_tokens_reserved())
        if token_return == None:
            self.position = position_aux
            token_return = self.get_token_value(Tokenizer.get_tokens_regex())

        token_value = token_return[0]
        token_type = token_return[1]

        if token_value.endswith('\n'):
            token_value = token_value.replace('\n','')
            self.position -= 1


        if ' ' in token_value and token_type != 'string':
            token_value = token_value.replace(' ','')

        if token_value[-1] == '(' and token_type != 'open_parentheses':
            self.position -= 1

        if token_value[-1] == '{' and token_type != 'open_block':
            self.position -= 1

        
        self.actual = Token(token_type)
        self.actual.value = token_value

        

class Pre_proc():
    def remove_comments(code):
        code = re.sub(re.compile("\/\*.*?\*\/|\/\/.*?\n",re.DOTALL) ,"" ,code)
        return code

class Parser:
    @staticmethod
    def parseProgram(tokenizer):
        commands = Commands(None,'commands')
        if tokenizer.actual.type == 'open_program':
            tokenizer.selectNext()
            while tokenizer.actual.type != 'close_program':
                commands.children.append(Parser.parseCommand(tokenizer))
                tokenizer.selectNext()

        return commands


    @staticmethod
    def parseBlock(tokenizer):
        node_root = Node(None,'block')
        block_root = Commands(node_root,'block')

        if tokenizer.actual.type == 'open_block':
            tokenizer.selectNext()

            while tokenizer.actual.type != 'close_block':
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
            command = Assignment(tokenizer.actual.value, tokenizer.actual.type)
            identifier = Identifier(tokenizer.actual.value, tokenizer.actual.type)
            command.children.append(identifier)
            tokenizer.selectNext()

            if tokenizer.actual.type == 'assignment':
                tokenizer.selectNext()
                
                command.children.append(Parser.parseRelexpr(tokenizer))
                return command


        elif tokenizer.actual.type == 'echo':
            command = Echo(tokenizer.actual.value, tokenizer.actual.type)
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))
            
            if tokenizer.actual.type != 'semi-collon':
                raise TypeError
            return command


        elif tokenizer.actual.type == 'while':
            command = While(tokenizer.actual.value, tokenizer.actual.type)
            tokenizer.selectNext()

            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()

            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.type != 'close_parentheses':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.type == 'open_block':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.type != 'close_block':
                    raise TypeError
            else:
                command.children.append(Parser.parseBlock(tokenizer))


            return command
            
        elif tokenizer.actual.type == 'if':
            command = If(tokenizer.actual.value,'if')
            tokenizer.selectNext()

            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()
            command.children.append(Parser.parseRelexpr(tokenizer))

            if tokenizer.actual.type != 'close_parentheses':
                raise TypeError
            tokenizer.selectNext()

            if tokenizer.actual.type == 'open_block':
                command.children.append(Parser.parseBlock(tokenizer))
                if tokenizer.actual.type != 'close_block':
                    raise TypeError
            else:
                command.children.append(Parser.parseCommand(tokenizer))

            tokenizer_next = copy.copy(tokenizer)
            tokenizer_next.selectNext()
            if tokenizer_next.actual.type == 'else':
                tokenizer.selectNext()
                tokenizer.selectNext()
                if tokenizer.actual.type == 'open_block':
                    command.children.append(Parser.parseBlock(tokenizer))
                    if tokenizer.actual.type != 'close_block':
                        raise TypeError
                else:
                    command.children.append(Parser.parseCommand(tokenizer))
            

            return command

        elif tokenizer.actual.type == 'funcdec':

            tokenizer.selectNext()
            if tokenizer.actual.type != 'function':
                raise TypeError

            func_name = tokenizer.actual.value
            command = FuncDec(func_name,'funcdec')
            tokenizer.selectNext()


            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()

            while tokenizer.actual.type != 'close_parentheses':
                identifier = Identifier(tokenizer.actual.value, tokenizer.actual.type)
                command.children.append(identifier)
                tokenizer.selectNext()

                while tokenizer.actual.type == 'comma':
                    tokenizer.selectNext()
                    identifier = Identifier(tokenizer.actual.value, tokenizer.actual.type)
                    command.children.append(identifier)
                    tokenizer.selectNext()
                
            tokenizer.selectNext()

            
            if tokenizer.actual.type == 'open_block':
                    command.children.append(Parser.parseBlock(tokenizer))

                    if tokenizer.actual.type != 'close_block':
                        raise TypeError
            else:
                raise TypeError

            return command

        elif tokenizer.actual.type == 'function':
            func_name = tokenizer.actual.value
            command = FuncCall(func_name,'funccall')
            tokenizer.selectNext()
            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()

            while tokenizer.actual.type != 'close_parentheses':
                command.children.append(Parser.parseRelexpr(tokenizer))

                while tokenizer.actual.type == 'comma':
                    tokenizer.selectNext()
                    command.children.append(Parser.parseRelexpr(tokenizer))
                
            return command
        
        elif tokenizer.actual.type == 'return':
            tokenizer.selectNext()
            command = Return(tokenizer.actual.value,tokenizer.actual.type)
            command.children.append(Parser.parseRelexpr(tokenizer))

            return command

        elif tokenizer.actual.type == 'semi-collon':
            return NoOp(None,None)

        else:
            command = Parser.parseBlock(tokenizer)
            return command

    @staticmethod
    def parseRelexpr(tokenizer):
        node = Parser.parseExpression(tokenizer)
        relexpr_root = node

        
        while tokenizer.actual.type == 'equals' or tokenizer.actual.type == 'greater' or tokenizer.actual.type == 'less' or tokenizer.actual.type == 'notequals':
            if len(relexpr_root.children) == 2:
                relexpr_root_aux = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                relexpr_root_aux.children.append(relexpr_root)
                tokenizer.selectNext()
                relexpr_root_aux.children.append(Parser.parseFactor(tokenizer))
                relexpr_root = relexpr_root_aux
            else:
                relexpr_root = BinOp(tokenizer.actual.value,tokenizer.actual.type)
                relexpr_root.children.append(node)
                tokenizer.selectNext()
                relexpr_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return relexpr_root
        
    @staticmethod
    def parseExpression(tokenizer):
        node = Parser.parseTerm(tokenizer)
        root = node

        while tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'or' or tokenizer.actual.type == 'concat':
                if len(root.children) == 2:
                    root_aux = BinOp(tokenizer.actual.value,tokenizer.actual.type)
                    root_aux.children.append(root)
                    tokenizer.selectNext()
                    root_aux.children.append(Parser.parseTerm(tokenizer))
                    root = root_aux
                else:
                    root = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                    root.children.append(node)
                    tokenizer.selectNext()
                    root.children.append(Parser.parseTerm(tokenizer))           
        return root

    @staticmethod
    def parseTerm(tokenizer):
        node = Parser.parseFactor(tokenizer)
        term_root = node
        tokenizer.selectNext()

        
        while tokenizer.actual.type == 'mult' or tokenizer.actual.type == 'div' or tokenizer.actual.type == 'and':
            if len(term_root.children) == 2:
                term_root_aux = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                term_root_aux.children.append(term_root)
                tokenizer.selectNext()
                term_root_aux.children.append(Parser.parseFactor(tokenizer))
                term_root = term_root_aux
            else:
                term_root = BinOp(tokenizer.actual.value, tokenizer.actual.type)
                term_root.children.append(node)
                tokenizer.selectNext()
                term_root.children.append(Parser.parseFactor(tokenizer))
            tokenizer.selectNext()

        return term_root

    @staticmethod
    def parseFactor(tokenizer):
        resultado = 0

        if tokenizer.actual.type == 'int':
            factor_root = IntVal(int(tokenizer.actual.value),tokenizer.actual.type)
            return factor_root
        if tokenizer.actual.type == 'function':
            func_name = tokenizer.actual.value
            command = FuncCall(func_name,'funccall')
            tokenizer.selectNext()
            if tokenizer.actual.type != 'open_parentheses':
                raise TypeError
            tokenizer.selectNext()

            while tokenizer.actual.type != 'close_parentheses':
                command.children.append(Parser.parseRelexpr(tokenizer))

                while tokenizer.actual.type == 'comma':
                    tokenizer.selectNext()
                    command.children.append(Parser.parseRelexpr(tokenizer))
                
            return command
        elif tokenizer.actual.type == 'true' or tokenizer.actual.type == 'false':
            if tokenizer.actual.type == 'true':
                factor_root = BoolVal(True, tokenizer.actual.type)
            else:
                factor_root = BoolVal(False, tokenizer.actual.type)
            return factor_root
        elif tokenizer.actual.type == 'string':
            tokenizer.actual.value = tokenizer.actual.value.replace('"','')
            factor_root = StringVal(str(tokenizer.actual.value),tokenizer.actual.type)
            return factor_root
        
        elif tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'not' or tokenizer.actual.type == 'open_parentheses' or tokenizer.actual.type == 'close_parentheses' or tokenizer.actual.type == 'identifier' or tokenizer.actual.type == 'readline':
            if tokenizer.actual.type == 'plus' or tokenizer.actual.type == 'minus' or tokenizer.actual.type == 'not':
                factor_root = UnOp(tokenizer.actual.value, tokenizer.actual.type)
                tokenizer.selectNext()
                factor_root.children.append(Parser.parseFactor(tokenizer))

        
            elif tokenizer.actual.type == 'open_parentheses':
                tokenizer.selectNext()
                factor_root = Parser.parseRelexpr(tokenizer)

                if(tokenizer.actual.type != 'close_parentheses'):
                    raise TypeError

            elif tokenizer.actual.type == 'identifier':
                factor_root = Identifier(tokenizer.actual.value, tokenizer.actual.type)

            elif tokenizer.actual.type == 'readline':
                factor_root = Readline(tokenizer.actual.value, tokenizer.actual.type)

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
        ast = Parser.parseProgram(tokenizer)
        symboltable = SymbolTable()
        ast.Evaluate(symboltable)
        

def main():
    source = sys.argv[1]
    Parser.run(source)


if __name__== "__main__":
  main()
