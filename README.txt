# TINY Language Compiler
### Scanner & Recursive Descent Parser with Syntax Tree Visualization

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Parsing-Recursive%20Descent-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/AST-Graphviz-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/License-Academic-lightgrey?style=flat-square" />
</p>

---

## Overview

This repository contains a **compiler front-end implementation** for the **TINY programming language**, developed using **Python**.  
The project implements the **Lexical Analysis** and **Syntax Analysis** phases of compilation and provides a **graphical user interface (GUI)** for interactive execution and visualization.

The compiler constructs an **Abstract Syntax Tree (AST)** using a **Recursive Descent Parser** and visualizes it using **Graphviz**, making the project well-suited for **compiler design education**.

---

## Key Features

- Lexical analysis using a finite-state scanner
- Recursive descent parsing based on the TINY grammar
- Abstract Syntax Tree (AST) construction
- Graph-based AST visualization using Graphviz
- Integrated graphical user interface (GUI)
- Step-by-step and full-pipeline execution
- Lexical and syntax error reporting
- Light and dark theme support

---

## System Architecture

The compiler front-end is organized into three main components:

### Scanner
- Converts source code into a sequence of tokens
- Handles keywords, identifiers, numbers, and operators
- Ignores comments enclosed in `{ ... }`
- Reports lexical errors

### Parser
- Implements recursive descent parsing
- Validates grammar rules
- Builds the Abstract Syntax Tree (AST)
- Reports syntax errors with contextual information

### Graphical User Interface
- Source code editor
- Scanner output panel
- Parser input panel
- Syntax tree visualization window

---

## Supported TINY Grammar

### Statements
- `if`
- `repeat`
- `read`
- `write`
- Assignment (`:=`)

### Control Structures
```text
if <exp> then <stmt-seq> [else <stmt-seq>] end
repeat <stmt-seq> until <exp>
