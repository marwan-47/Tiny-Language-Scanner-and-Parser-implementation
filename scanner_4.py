import argparse
List = []
terminator=[' ','\n','\t']
reserved_words = ["if", "then", "else", "end", "repeat", "until", "read", "write"]  
i=-1
def add_token(token_type, token_value):
    """Add a token dictionary to the list"""
    token = {
        "type": token_type,
        "value": token_value
    }
    List.append(token)
    return 1    
def special_words(c):
    state_flag=0
    if c == ';':
        state_flag=add_token("SEMICOLON", c)
    elif c == '=':
        state_flag=add_token("EQUAL", c)
    elif c == '<':
        state_flag=add_token("LESSTHAN", c)
    elif c == '+':
        state_flag=add_token("PLUS", c)
    elif c == '-':
        state_flag=add_token("MINUS", c)
    elif c == '*':
        state_flag=add_token("MULT", c)
    elif c == '/':
        state_flag=add_token("DIV", c)
    elif c == '(':
        state_flag=add_token("OPENBRACKET", c)
    elif c == ')':
        state_flag=add_token("CLOSEDBRACKET", c)
    return state_flag

def get_token(content):
                global i
                state = "Start"
                history = ""
                line_number = 1
                content_length=len(content)
                state_flag=0
                while(i<content_length-1 and not state_flag):
                    i+=1
                    c=content[i]
                    if c == '\n':
                        line_number += 1
                    if state =="Start":
                        state_flag=special_words(c)
                        if state_flag:
                            state="Start"
                            continue
                        elif c==":":
                            state="Colon"
                        elif c.isdigit():
                            state="Digit"
                            history += c
                        elif c.isupper():
                            state="Identifier"
                            history += c
                        elif c.islower():
                            state="Letters"
                            history += c
                        elif c=="{":
                            state="Comment"
                        elif c in terminator:
                            continue
                        else:
                            raise Exception(f"Invalid Character '{c}' ")
                    elif state=="Comment":
                        if c=="}":
                            state="Start"
                        else:
                            continue
                    elif state=="Colon":
                        if c=="=":
                            state_flag=add_token("ASSIGN", ":=")
                            state="Start"
                        else:
                            raise Exception(f"Invalid token, expected '=' after ':' ")
                    elif state=="Digit":
                        if c.isdigit():
                            history += c
                        else:
                            state_flag=add_token("NUMBER", history)
                            state="Start"
                            i-=1
                    elif state=="Identifier":
                        if c.isalpha():
                            history += c
                        else:
                            state_flag=add_token("IDENTIFIER", history)
                            state="Start"
                            i+=-1
                    elif state=="Letters":
                        if c.isupper():
                            history += c
                            state="Identifier"
                        elif c.islower():
                            history += c
                        elif history in reserved_words:
                            state_flag=add_token(history.upper(), history)
                            i-=1
                            state = "Start"
                        else:
                            state_flag=add_token("IDENTIFIER", history)
                            state="Start"
                            i-=1
                    if c in terminator:
                        continue
                if(i>=content_length-1):
                    if state == "Comment":
                        raise Exception(f"Unclosed comment ")
                    elif state == "Colon":
                        raise Exception(f"Expected '=' after ':' ")
                    elif state == "Digit" and history:
                        add_token("NUMBER", history)
                    elif state == "Identifier" and history:
                        add_token("IDENTIFIER", history)
                    elif state == "Letters" and history:
                        if history in reserved_words:
                            add_token(history.upper(), history)
                        else:
                            add_token("IDENTIFIER", history)
                return i == content_length-1 

def get_all_token(content):
    global i
    i=-1
    while(not get_token(content)):continue
def open_file(filename):
    """Read file character by character and tokenize"""
    try:
        with open(filename, 'r') as file:
            content = file.read()
            get_all_token(content)
            # print("Token List:")
            # print(List)
    except FileNotFoundError:
        print(f"\033[91mERROR: File '{filename}' not found.\033[0m")
        raise Exception(f"File '{filename}' not found.")
    except Exception as e:
        print(f"\033[91mERROR: {e}\033[0m")
        raise

####some bullshit for CMD
# import argparse
# import os
# import sys

# # --- helpers to work with your global scanner state ---
# def reset_scanner():
#     global i, List
#     i = -1
#     List.clear()

# def load_content(path: str) -> str:
#     if path == "-" or path == "/dev/stdin":
#         return sys.stdin.read()
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()

# def run_all(content: str):
#     reset_scanner()
#     get_all_token(content)
#     # print tokens
#     for t in List:
#         print(f"{t['type']:>12}  {t['value']}")

# def run_step(content: str, steps: int):
#     """
#     Execute get_token() up to `steps` times (or until EOF).
#     Prints the newly produced token each step.
#     """
#     reset_scanner()
#     produced = 0
#     while produced < steps:
#         before = len(List)
#         eof = get_token(content)
#         after = len(List)
#         if after > before:
#             t = List[-1]
#             print(f"{t['type']:>12}  {t['value']}")
#             produced += 1
#         if eof:
#             # flush is already handled inside get_token on EOF
#             break

# def repl(content: str):
#     """
#     Interactive stepping: 'n' = next token, 'a' = rest, 'p' = print all so far,
#     'r' = reset and start over, 'q' = quit.
#     """
#     reset_scanner()
#     print("Interactive mode. Commands: [n]ext, [a]ll, [p]rint, [r]eset, [q]uit")
#     while True:
#         cmd = input("> ").strip().lower()
#         if cmd in ("q", "quit", "exit"):
#             break
#         elif cmd in ("p", "print"):
#             for t in List:
#                 print(f"{t['type']:>12}  {t['value']}")
#         elif cmd in ("r", "reset"):
#             reset_scanner()
#             print("Scanner reset.")
#         elif cmd in ("a", "all"):
#             # finish the rest
#             while not get_token(content):
#                 pass
#             # tokens are all in List now
#             print(f"Done. {len(List)} tokens total.")
#         elif cmd in ("n", "next", ""):
#             before = len(List)
#             eof = get_token(content)
#             after = len(List)
#             if after > before:
#                 t = List[-1]
#                 print(f"{t['type']:>12}  {t['value']}")
#             if eof:
#                 print("EOF reached.")
#         else:
#             print("Unknown command. Use n/a/p/r/q.")

# def main():
#     parser = argparse.ArgumentParser(
#         description="Tiny language scanner CLI: batch, step, or interactive."
#     )
#     parser.add_argument(
#         "file",
#         nargs="?",
#         default="file.txt",
#         help="Path to input file (use '-' for stdin). Default: file.txt",
#     )
#     mode = parser.add_mutually_exclusive_group()
#     mode.add_argument("--all", action="store_true", help="Tokenize the whole file.")
#     mode.add_argument("--step", type=int, metavar="N",
#                       help="Produce N tokens then stop.")
#     mode.add_argument("--repl", action="store_true",
#                       help="Interactive stepping REPL.")
#     args = parser.parse_args()

#     # load input
#     try:
#         content = load_content(args.file)
#     except FileNotFoundError:
#         print(f"ERROR: file not found: {args.file}", file=sys.stderr)
#         sys.exit(1)

#     # choose mode (default = --all)
#     if args.repl:
#         repl(content)
#     elif args.step is not None:
#         run_step(content, args.step)
#     else:
#         run_all(content)

# if __name__ == "__main__":
#     main()


# === Wrappers used by parser / GUI ===
def reset_scanner():
    """Reset global state before each new scan."""
    global i, List
    try:
        i
    except NameError:
        # if i not defined yet, just initialize
        i = -1
    try:
        List
    except NameError:
        List = []
    i = -1
    List.clear()

def scan_text(text: str):
    """Scan source text and return a NEW list of token dicts."""
    reset_scanner()
    get_all_token(text)
    return List.copy()

def scan_file(path: str):
    """Scan a file and return token list."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return scan_text(content)
