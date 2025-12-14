
This fixed version removes the syntax error in parser_core.py.

- parser_core.py:
    * Parser implementation
    * ast_to_str_book(ast): prints tree with nodes exactly like the textbook figure
      (no 'program' or 'stmt_sequence' levels).

- tiny_gui.py:
    * GUI that takes TINY source, runs scanner_4.scan_text, then parser,
      and prints the textbook-style syntax tree.

Make sure your scanner_4.py defines:

    def scan_text(src: str) -> list[dict]:
        # returns [{'type': 'READ', 'value': 'read'}, ...]
