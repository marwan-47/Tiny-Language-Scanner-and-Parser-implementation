
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Token:
    type: str
    value: str
#dh 8rdo y7wl al token alli gia mn scanner l object mn type w value
@dataclass #m3nha dih data class msh m7tag aktb __init__
class ASTNode:
    kind: str #no3 node fi parse tree msln if wla repeat
    value: Optional[str] = None
    children: List["ASTNode"] = field(default_factory=list)

    def add(self, child: "ASTNode") -> "ASTNode":
        self.children.append(child)
        return self
#mn a5r dih AST 7rfin btbni tree a2ol 7aga no3 node fi tree msln hya if wla aassign wla no3 omha aih b3dha value msln lw if aih value wla 7aga 34an if nfsha node w 5las momkn lw identifier msln al value tb2a x w hkza34an k2a 2ail optional[str]=none y3ni momkn ykon str aw none , fi b3dha children bta3t tree w dh mntqi l ai node lihe children w akid mn no3 AST 34an dih bt3br 3n simple node 7ta 7oar field(default_factory=list) dih 7nika 34an avoid mutation w a5irn ank t add children ll node mn 5lal add method tb lih 7tin 'ASTNode' dih asmha forward referncing 34an till nw al astnode lsa didnt created f ani a2olk mn no3 dh goa class alli lsa b create hy7df fi w4k error 2la la khlas h3ml forward referencing y3ni na refernce type will exist later 
class ParserError(Exception):
    pass
#dh 8rdo lw fi parser error yrmi error w ytrmi fi gui
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens #sequeunce of tokens from scanner 
        self.pos = 0 #na fin 7alin fi parser 

    @property#34an access k parameter msh k method mogrd tzoi2
    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "")
    #dh 8rdo y check lw position bta3i a2l mn length tokens bta3t scanner f na kda fi aman 8ir dka rg3 eof y3ni enough kda 5las
    def advance(self) -> None:
        self.pos += 1#dh 8rdo y7rk al pointer k scanning al parsing 
    def match(self, *expected_types: str) -> Token:
        tok = self.current
        if tok.type in expected_types:
            self.advance()
            return tok
        raise ParserError(
            f"Expected {expected_types} but found {tok.type} ({tok.value}) "
        )
#mn a5r dih match 3adi tok bt2ol na wa2f 3la aih b3dha b3ml check hl alli na wa2f 3lih hwa al expected lw ah advance w rg3o lih brg3o 34an w na bbni al syntax tree 8ir kda armi error
    def parse(self) -> ASTNode:
        root = self.parse_program()
        if self.current.type != "EOF":
            raise ParserError(
                f"Unexpected token after program end: {self.current.type} ({self.current.value})"
            )
        return root
#dih official start of the parser , al mafrod b3d ma a5ls parse program ykon kol alli fi token list 5ls lw fi 7aga m5lst4 a7df error 
    # program = stmt_sequence ;
    def parse_program(self) -> ASTNode:
        stmts = self.parse_stmt_sequence(stop_tokens={"EOF"})
        return ASTNode("program").add(stmts)

    # stmt_sequence = statement { ';' statement } ;
    def parse_stmt_sequence(self, stop_tokens=None) -> ASTNode:
        if stop_tokens is None:
            stop_tokens = set() #m3nha lw mfi4 specified a3ml empty w dih 7rs msh aktr bs msh fr2a y3ni 
        stmts: List[ASTNode] = [self.parse_statement()]
        while True:
            if self.current.type == "SEMICOLON":
                self.advance()#na hna b advance da5li 3adi lw 3mlt match bs msh fr2a 7sitha ashl
                if self.current.type in stop_tokens or self.current.type == "EOF":
                    break
                stmts.append(self.parse_statement())
            else:
                break
        return ASTNode("stmt_sequence", children=stmts)
#tib 4r7 al qsa dih b2a w7da w7da na hna m7tag 7aga zi follow set so2al lih bbsata 34an na 3mal a parse h2of amta msh 3arf h2of lma a4of msln else s3tha kda 5las al grammar rule dih k2ni b7rf 7dod li amta h2of , tmm b3dha b2a 3rft 3adi list[ASTNode] w dih 34an lma arg3 al AST dih code al chapter
    # statement = if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt ;
    def parse_statement(self) -> ASTNode:
        tok = self.current
        if tok.type == "IF":
            return self.parse_if_stmt()
        elif tok.type == "REPEAT":
            return self.parse_repeat_stmt()
        elif tok.type == "IDENTIFIER":
            return self.parse_assign_stmt()
        elif tok.type == "READ":
            return self.parse_read_stmt()
        elif tok.type == "WRITE":
            return self.parse_write_stmt()
        raise ParserError(f"Unexpected token {tok.type} ({tok.value}) at start of statement")
#dih shala msh m7taga 4r7
    # if_stmt = "if" exp "then" stmt_sequence [ "else" stmt_sequence ] "end" ;
    def parse_if_stmt(self) -> ASTNode:
        self.match("IF")
        cond = self.parse_exp()
        self.match("THEN")
        then_seq = self.parse_stmt_sequence(stop_tokens={"ELSE", "END"})
        else_seq: Optional[ASTNode] = None
        if self.current.type == "ELSE":
            self.advance()
            else_seq = self.parse_stmt_sequence(stop_tokens={"END"})
        self.match("END")
        node = ASTNode("if")
        node.add(cond).add(then_seq)
        if else_seq is not None:
            node.add(else_seq)
        return node

    # repeat_stmt = "repeat" stmt_sequence "until" exp ;
    def parse_repeat_stmt(self) -> ASTNode:
        self.match("REPEAT")
        body = self.parse_stmt_sequence(stop_tokens={"UNTIL"})
        self.match("UNTIL")
        cond = self.parse_exp()
        node = ASTNode("repeat")
        node.add(body).add(cond)
        return node

    # assign_stmt = identifier ':=' exp ;
    def parse_assign_stmt(self) -> ASTNode:
        ident = self.match("IDENTIFIER")
        self.match("ASSIGN")
        expr = self.parse_exp()
        node = ASTNode("assign", value=ident.value)
        node.add(expr)
        return node

    # read_stmt = 'read' identifier ;
    def parse_read_stmt(self) -> ASTNode:
        self.match("READ")
        ident = self.match("IDENTIFIER")
        return ASTNode("read", value=ident.value)

    # write_stmt = 'write' exp ;
    def parse_write_stmt(self) -> ASTNode:
        self.match("WRITE")
        expr = self.parse_exp()
        node = ASTNode("write")
        node.add(expr)
        return node

    # exp = simple_exp [ comparison_op simple_exp ] ;
    def parse_exp(self) -> ASTNode:
        left = self.parse_simple_exp()
        if self.current.type in ("LESSTHAN", "LESS_THAN", "EQUAL", "EQUALS"):
            op_tok = self.current
            self.advance()
            right = self.parse_simple_exp()
            node = ASTNode("op", value=op_tok.value)
            node.add(left).add(right)
            return node
        return left

    # simple_exp = term { addop term } ;
    def parse_simple_exp(self) -> ASTNode:
        node = self.parse_term()
        while self.current.type in ("PLUS", "MINUS"):
            op_tok = self.current
            self.advance()
            rhs = self.parse_term()
            op_node = ASTNode("op", value=op_tok.value)
            op_node.add(node).add(rhs)
            node = op_node
        return node

    # term = factor { mulop factor } ;
    def parse_term(self) -> ASTNode:
        node = self.parse_factor()
        while self.current.type in ("MULT", "DIV"):
            op_tok = self.current
            self.advance()
            rhs = self.parse_factor()
            op_node = ASTNode("op", value=op_tok.value)
            op_node.add(node).add(rhs)
            node = op_node
        return node

    # factor = '(' exp ')' | number | identifier ;
    def parse_factor(self) -> ASTNode:
        tok = self.current
        if tok.type == "OPENBRACKET":
            self.advance()
            n = self.parse_exp()
            self.match("CLOSEDBRACKET")
            return n
        if tok.type == "NUMBER":
            self.advance()
            return ASTNode("const", value=tok.value)
        if tok.type == "IDENTIFIER":
            self.advance()
            return ASTNode("id", value=tok.value)
        raise ParserError(f"Unexpected token in factor: {tok.type} ({tok.value})")

def ast_to_str_book(node: ASTNode, indent: str = "") -> str:
    """Text tree similar to textbook, hiding program/stmt_sequence nodes."""
    if node.kind in {"program", "stmt_sequence"}:
        return "\n".join(ast_to_str_book(c, indent) for c in node.children)
    label = node.kind
    if node.value is not None:
        label += f" ({node.value})"
    lines = [indent + label]
    for child in node.children:
        lines.append(ast_to_str_book(child, indent + "  "))
    return "\n".join(lines)
#dh mlhoash lzma
def build_ast_from_token_dicts(token_dicts: List[dict]) -> ASTNode:
    tokens = [Token(t["type"], t["value"]) for t in token_dicts]
    return Parser(tokens).parse()
#dh y7wl al scanner l token objects w y initiate al parser 