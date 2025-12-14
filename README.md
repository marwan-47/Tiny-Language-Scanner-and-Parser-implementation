Here is a professional, clean, and comprehensive `README.md` file designed specifically for your codebase. It highlights the features, explains the installation of the critical Graphviz dependency, and documents the grammar.

***

# TINY Language Compiler & Visualizer

A robust compiler frontend for the **TINY** language, featuring a custom Lexical Analyzer (Scanner) and a Recursive Descent Parser. The project includes a modern **GUI** built with Tkinter that visualizes the Syntax Tree using Graphviz.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Educational-orange)

## Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [TINY Language Grammar](#-tiny-language-grammar)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

## Overview

This project implements the first two phases of a compiler for the TINY educational language:

1.  **Scanner (`scanner_4.py`):** Reads source code character-by-character and groups them into tokens (Reserved words, Identifiers, Numbers, Symbols).
2.  **Parser (`parser_core.py`):** Takes the token stream and builds an Abstract Syntax Tree (AST) using recursive descent logic.
3.  **Visualization (`tiny_gui.py`):** A graphical interface that allows users to write code, view tokens, and interactively explore the generated Syntax Tree.

## Features

*   **Full Pipeline Visualization:** View Source Code, Token Lists, and the Syntax Tree side-by-side.
*   **Interactive Syntax Tree:** 
    *   High-quality rendering using **Graphviz**.
    *   **Zoom & Pan** capabilities for navigating large trees.
    *   Distinguishes between statement links (horizontal) and nesting (vertical).
*   **Modern GUI:**
    *   **Dark / Light Theme** toggle.
    *   Syntax highlighting support (via structure).
    *   File Save/Load functionality.
*   **Error Handling:** Reports lexical errors (e.g., unclosed comments) and syntax errors (e.g., missing semicolons).

## Prerequisites

To run this application, you must have the following installed:

1.  **Python 3.8 or higher**
2.  **Graphviz (System Binary)**  
    *The Python code generates a `.dot` file, but the `dot` executable is required to render it into an image.*
    *   **Windows:** [Download Installer](https://graphviz.org/download/).  
        *⚠️ Important:* During installation, select **"Add Graphviz to the system PATH for all users"**.
    *   **Linux:** `sudo apt install graphviz`
    *   **Mac:** `brew install graphviz`

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/tiny-compiler.git
    cd tiny-compiler
    ```

2.  **Install Python requirements:**
    ```bash
    pip install graphviz pillow
    ```

## Usage

1.  **Launch the GUI:**
    ```bash
    python tiny_gui.py
    ```

2.  **Run the Compiler:**
    *   **Write Code:** Type TINY code into the "TINY Source" text box (or use the "Load Source File" button).
    *   **Scan & Parse:** Click the **"Scanner + Parser (Full Pipeline)"** button.
    *   **Visualize:** A new window will appear displaying the Syntax Tree. You can zoom in/out with the scroll wheel or on-screen buttons.

### Example TINY Code
```pascal
{ Sample Factorial Program }
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

## TINY Language Grammar

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

## Project Structure

| File | Description |
| :--- | :--- |
| `tiny_gui.py` | The main entry point. Handles the UI, Graphviz rendering logic, and themes. |
| `scanner_4.py` | State-machine implementation for tokenizing TINY source code. |
| `parser_core.py` | Defines `ASTNode` and the `Parser` class which consumes tokens to build the tree. |

## Troubleshooting

### "Graphviz dot.exe not found"
If you see an error claiming Graphviz is missing:
1.  Ensure you installed the **Graphviz software** (not just the pip library).
2.  **Windows Users:** Check if `C:\Program Files\Graphviz\bin` is in your System Environment Variables (PATH).
3.  Restart your IDE or terminal after installing Graphviz.

### PyInstaller / Exe Issues
The code includes specific helpers (`_fix_runtime_paths`, `ensure_dot_available`) to help bundle this application as an executable. If building with PyInstaller, ensure you include the Graphviz `bin` folder and Tcl/Tk libs in the spec file.

---

*Developed for the Compiler Construction Course.*
