Here is a professional, well-structured `README.md` file tailored to your project. It covers installation, usage, technical details (BNF grammar), and troubleshooting, which is essential for projects involving Graphviz.

***

# TINY Language Compiler & Visualizer

A Python-based compiler frontend for the **TINY** language. This project implements a **Scanner** (Lexical Analyzer) and a **Recursive Descent Parser** with a full GUI to visualize the generating Syntax Tree using Graphviz.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Educational-orange)

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [TINY Language Grammar](#-tiny-language-grammar)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

## 📖 Overview

This application reads source code written in the TINY language and performs two major compilation phases:
1.  **Scanning:** Tokenizes the source code into a sequence of lexemes and token types (Keywords, Identifiers, Numbers, Operators).
2.  **Parsing:** Constructs an Abstract Syntax Tree (AST) using a recursive descent approach and generates a visual representation of the Syntax Tree.

It is designed for educational purposes to demonstrate compiler construction concepts.

## ✨ Features

*   **GUI Interface:** A user-friendly Tkinter-based interface with **Dark/Light mode** support.
*   **Lexical Analysis:** Identifies reserved words (`if`, `then`, `repeat`, etc.), special symbols, numbers, and identifiers.
*   **Syntax Analysis:** Validates grammar and builds an AST.
*   **Visualizer:** Renders the Syntax Tree using **Graphviz** with high-quality PNG output.
*   **Interactive View:** Zoom and pan controls for inspecting large Syntax Trees.
*   **Pipeline Control:** Run the Scanner only, Parser only, or the full pipeline at once.
*   **File Handling:** Save/Load source files and token lists.

## ⚙️ Prerequisites

To run this project, you need the following:

1.  **Python 3.8+**
2.  **Graphviz (System Binary):** The software relies on the `dot` command.
    *   *Windows:* Download the installer from [graphviz.org](https://graphviz.org/download/). **Important:** During installation, select "Add Graphviz to the system PATH for all users."
    *   *Linux/Mac:* `sudo apt install graphviz` or `brew install graphviz`.
3.  **Python Packages:**
    *   `graphviz` (Python wrapper)
    *   `Pillow` (Image processing)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/tiny-compiler.git
    cd tiny-compiler
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install graphviz pillow
    ```

3.  **Verify Graphviz:**
    Open your terminal and type `dot -V`. If it returns a version number, you are ready to go.

## 🚀 Usage

1.  **Run the GUI:**
    ```bash
    python tiny_gui.py
    ```

2.  **Workflow:**
    *   **Step 1:** Paste your TINY code into the "TINY Source" box or click **Load Source File**.
    *   **Step 2:** Click **Scanner + Parser (Full Pipeline)** to see immediate results.
    *   **Step 3:** A new window will pop up showing the generated Syntax Tree. Use the scroll wheel to zoom.

### Example TINY Code
```pascal
read x;
if 0 < x then
  fact := 1;
  repeat
    fact := fact * x;
    x := x - 1
  until x = 0;
  write fact
end
```

## 📐 TINY Language Grammar

The parser implements the following BNF (Backus-Naur Form) grammar:

```ebnf
program       ::= stmt_sequence
stmt_sequence ::= statement { ";" statement }
statement     ::= if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
if_stmt       ::= "if" exp "then" stmt_sequence [ "else" stmt_sequence ] "end"
repeat_stmt   ::= "repeat" stmt_sequence "until" exp
assign_stmt   ::= identifier ":=" exp
read_stmt     ::= "read" identifier
write_stmt    ::= "write" exp
exp           ::= simple_exp [ ("<" | "=") simple_exp ]
simple_exp    ::= term { ("+" | "-") term }
term          ::= factor { ("*" | "/") factor }
factor        ::= "(" exp ")" | number | identifier
```

## 📂 Project Structure

```text
.
├── scanner_4.py      # Lexical Analyzer logic (StateMachine implementation)
├── parser_core.py    # Recursive Descent Parser & AST Node definitions
├── tiny_gui.py       # Main Entry Point & Tkinter GUI
└── README.md         # Documentation
```

## 🔧 Troubleshooting

**Error: "Graphviz dot.exe not found"**
1.  Ensure you have installed the Graphviz **software** (not just the pip package).
2.  On Windows, check your environment variables to ensure `C:\Program Files\Graphviz\bin` (or similar) is in your **PATH**.
3.  Restart your IDE or Terminal after installing Graphviz.

**Error: "Unclosed comment" or "Invalid Token"**
*   Ensure comments are enclosed in curly braces `{ comment }`.
*   Ensure assignment uses `:=` and checks for equality use `=`.

***

*Developed for the Compiler Construction Course.*
