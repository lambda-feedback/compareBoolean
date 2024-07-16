from .lex import Token, TokenType, Lexer
from .ast import Expr, Prod, Term

from sympy.logic.boolalg import Boolean, And, Or, Xor, Not
from sympy.core.symbol import symbols

class ParseError(Exception):

    def __init__(self, msg: str):
        self.msg = msg
    def __str__(self):
        return self.msg


class FeedbackException(Exception):

    def __str__(self):
        if isinstance(self.__cause__, ParseError):
            return str(self.__cause__)
        else:
            return "Evaluation failed"


def expect(tokens: list[Token], type: TokenType) -> bool:
    token = tokens.pop()
    if token.type == type:
        return True
    else:
        tokens.append(token)
        return False

# Grammar:
# expr = prod ([or | xor] prod)*
# prod = term (and term)*
# term = (unary) [variable | '(' expr ')']

def parse_term(tokens: list[Token]) -> Term:
    op = expect(tokens, TokenType.NOT)

    if tokens[-1].type == TokenType.VARIABLE:
        term = tokens.pop().value
        return Term(term, op)
    elif expect(tokens, TokenType.LBRACKET):
        try:
            term = parse_boolean(tokens)

            if not expect(tokens, TokenType.RBRACKET):
                raise ParseError("Expected closing \')\'")
            
            return Term(term, op)
        except:
            raise
    else:
        raise ParseError(f"Unexpected token \"{tokens[-1].text}\"")

def parse_prod(tokens: list[Token]) -> Prod:
    left = None
    try:
        left = parse_term(tokens)
    except:
        raise

    right = []
    while expect(tokens, TokenType.AND):
        try:
            new_right = parse_term(tokens)
            right.append(new_right)
        except:
            raise
    
    return Prod(left, right)

# A recursive descent parser
def parse_boolean(tokens: list[Token]) -> Expr:
    left = None
    try:
        left = parse_prod(tokens)
    except:
        raise
    
    right = []
    next_token = tokens[-1].type
    while expect(tokens, TokenType.OR) or expect(tokens, TokenType.XOR):
        try:
            new_right = parse_prod(tokens)
            right.append((next_token == TokenType.XOR, new_right))
            next_token = tokens[-1].type
        except:
            raise
    
    return Expr(left, right)

def parse_with_feedback(input: str, latex: bool = False) -> tuple[Expr, Boolean]:
    # Tokenise the input string
    tokens = Lexer(input).lex()
    # Attempt to parse the tokens into an AST
    try:
        expr = parse_boolean(list(reversed(tokens)))

        # Walk the tree, converting the result into a sympy boolean expression
        sympy_expr = conv_expr(expr)
        return expr, sympy_expr
    except Exception as e:
        raise FeedbackException from e

def conv_term(term: Term) -> Boolean:
    out = None
    # Is this term a variable?
    if isinstance(term.term, str):
        # If so, create a sympy symbol for it
        out = symbols(term.term)
    else:
        # If it isnt a variable, it must be a nested expression
        out = conv_expr(term.term)
    return Not(out) if term.op else out

def conv_prod(prod: Prod) -> Boolean:
    left = conv_term(prod.left)
    right_list = []
    for right in prod.right:
        right_list.append(conv_term(right))
    return And(left, *right_list)

def conv_expr(expr: Expr) -> Boolean:
    result = conv_prod(expr.left)
    for xor, right in expr.right:
        right = conv_prod(right)
        if xor:
            result = Xor(result, right)
        else:
            result = Or(result, right)
    return result
