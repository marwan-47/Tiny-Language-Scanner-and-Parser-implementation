🧩 TINY Language Compiler
🔍 Scanner & 🌳 Recursive Descent Parser with Syntax Tree Visualization
📄 Abstract

This project presents the design and implementation of a compiler front-end for the TINY programming language, developed using Python. The system implements two fundamental compilation phases: Lexical Analysis (Scanning) and Syntax Analysis (Parsing) using a Recursive Descent Parser.
A modern graphical user interface (GUI) built with Tkinter enables interactive source code editing, compilation pipeline execution, and visual exploration of the Abstract Syntax Tree (AST) using Graphviz.

This project is primarily intended for academic and educational use, particularly in Compiler Design and Programming Languages courses.

🎯 Objectives

The primary objectives of this project are to:

🔹 Implement a Lexical Analyzer for tokenizing TINY source code

🔹 Develop a Recursive Descent Parser that validates grammar rules

🔹 Construct a structured Abstract Syntax Tree (AST)

🔹 Provide an interactive GUI for compilation stages

🔹 Visualize syntax trees using Graphviz

🔹 Enhance conceptual understanding of compiler front-end design

🧠 System Overview

The compiler front-end is organized into three main components:

🔍 Scanner Module

Performs lexical analysis

Converts source code into a stream of tokens

Detects and reports lexical errors

🌳 Parser Module

Implements recursive descent parsing

Validates syntax according to TINY grammar

Builds the Abstract Syntax Tree (AST)

🖥️ GUI Module

Manages user interaction and file I/O

Displays scanner and parser outputs

Renders AST visualizations

✨ Features
🔎 Lexical Analysis

Token classification: keywords, identifiers, numbers, operators

Comment handling using { ... }

Clear and descriptive error messages

🌲 Recursive Descent Parsing

Full support for standard TINY grammar

AST generation with hierarchical structure

Syntax error detection with contextual feedback

🖼️ Syntax Tree Visualization

High-quality AST rendering via Graphviz

Zoom and pan support for large trees

🖥️ Graphical User Interface

Built-in TINY source code editor

Separate views for:

Scanner output (tokens)

Parser input

One-click Full Pipeline Execution

🌗 Dark / Light mode toggle

📐 Supported TINY Grammar
🧾 Statements

if

repeat

read

write

Assignment (:=)

🔁 Control Structures
if <exp> then <stmts> [else <stmts>] end
repeat <stmts> until <exp>

➕ Expressions

Arithmetic: + - * /

Relational: < =

💬 Comments
{ This is a comment }

🧪 Example TINY Program
read x;
if 0 < x then
  fact := 1;
  repeat
    fact := fact * x;
    x := x - 1
  until x = 0;
  write fact
end

📂 Project Structure
📁 File	📝 Description
tiny_gui.py	Main entry point and GUI controller
scanner_4.py	Lexical Analyzer implementation
parser_core.py	Recursive Descent Parser and AST logic

⚠️ Important
The parser file must be named exactly parser_core.py.
Incorrect naming will result in import errors.

🛠️ Installation & Requirements
🧰 Software Requirements

Python 3.x

Graphviz (system installation)

📦 Python Dependencies
pip install graphviz pillow


🐧 Linux users may need:

sudo apt-get install python3-tk

▶️ Execution Instructions
python tiny_gui.py


Steps:

Load or type TINY source code

Run the Scanner

Execute the Parser

View the generated Syntax Tree

Optionally run the Full Pipeline

🎓 Educational Value

This project demonstrates:

✔ Practical lexical and syntactic analysis

✔ Recursive descent parsing techniques

✔ Abstract Syntax Tree construction

✔ Integration of theory with a functional compiler tool

It is suitable for:

Compiler Design

Formal Languages

Programming Language Principles

🚧 Future Enhancements

🧠 Semantic analysis & symbol tables

🧾 Type checking

⚙ Intermediate code generation

🚀 Optimization phases

📤 AST export (JSON / XML)

📜 License

This project is intended for academic and educational use.
Users are free to modify and extend it for learning, teaching, and research purposes.

🤝 Contributions

Contributions are welcome.
Feel free to fork the repository, improve functionality, or extend compiler stages.
