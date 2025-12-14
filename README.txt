TINY Language Compiler - Scanner & Parser

A robust, Python-based compiler front-end for the TINY language. This project implements a Lexical Analyzer (Scanner) and a Recursive Descent Parser, wrapped in a modern Tkinter GUI that visualizes the Syntax Tree using Graphviz.

🚀 Features

Lexical Analysis: Scans TINY source code to generate a stream of tokens (Keywords, Operators, Identifiers, Literals).

Recursive Descent Parsing: Validates the token stream against the TINY grammar and builds an Abstract Syntax Tree (AST).

AST Visualization: Generates and displays high-quality graphical representations of the Syntax Tree using Graphviz.

Interactive GUI:

Built-in Text Editor for TINY source code.

Split-view for Scanner output (tokens) and Parser input.

Dark/Light Mode support.

Zoom and Pan controls for the Syntax Tree viewer.

Error Handling: Detailed error reporting for both lexical and syntactic errors.

🛠️ Prerequisites

Before running the application, ensure you have the following installed:

1. Python 3.x

Ensure Python is installed and added to your system PATH.

2. Graphviz (System Software)

This project requires the Graphviz software to render trees.

Windows: Download Installer. During installation, select "Add Graphviz to the system PATH for all users".

Linux: sudo apt-get install graphviz

Mac: brew install graphviz

3. Python Libraries

Install the required Python packages:

pip install graphviz pillow


(Note: tkinter is usually included with Python installations. If missing on Linux, install python3-tk)

📂 Project Structure

File

Description

tiny_gui.py

Entry Point. The main GUI application. Handles user interaction, file I/O, and invokes the scanner/parser.

scanner_4.py

The Scanner. Contains the state machine logic to tokenize TINY source code.

parser_core.py

The Parser. Defines the ASTNode structure and implements recursive descent logic to build the tree.

⚠️ Important: Ensure the parser file is named parser_core.py (not parser_core (1).py) so tiny_gui.py can import it correctly.

🏃‍♂️ How to Run

Clone or download this repository.

Open your terminal/command prompt in the project folder.

Run the GUI:

python tiny_gui.py


📖 Usage Guide

Load Source:

Click "Load Source File" to open a .txt file containing TINY code.

Alternatively, type or paste code directly into the "TINY Source" text box.

Scan:

Click "Run Scanner". The tokens will appear in the "Scanner Output" panel.

This output is automatically copied to the "Parser Input" panel.

Parse:

Click "Parse → Syntax Tree".

If the code is valid, a new window will pop up showing the generated Syntax Tree.

Full Pipeline:

Click "Scanner + Parser (Full Pipeline)" to run both steps instantly.

📝 TINY Language Grammar

This compiler supports the standard TINY grammar:

Statements: if, repeat, read, write, assignment (:=).

Conditions: if <exp> then <stmts> [else <stmts>] end.

Loops: repeat <stmts> until <exp>.

Expressions: Supports arithmetic (+, -, *, /) and comparison (<, =) operators.

Comments: Enclosed in curly braces { ... }.

Example Code

read x;
if 0 < x then
  fact := 1;
  repeat
    fact := fact * x;
    x := x - 1
  until x = 0;
  write fact
end


🎨 Themes

The GUI includes a toggle for Dark Mode and Light Mode (default). Click the "Toggle Dark/Light" button in the top right corner to switch themes.

🤝 Contributing

Feel free to fork this project and submit pull requests. Bug reports and feature suggestions are welcome.
