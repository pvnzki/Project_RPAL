# 📘 Project_RPAL

## 🧠 Introduction

Welcome to the **RPAL Interpreter** project!  
This is a complete implementation of an interpreter for the **Right-reference Pedagogic Algorithmic Language (RPAL)**, developed in Python.

The interpreter is modular, with the following key components:

- 🔹 **Lexical Analyzer**: Scans the RPAL source code and converts it into a stream of tokens. Tokens are fundamental units like keywords, identifiers, and operators.
- 🔹 **Parser**: Constructs an **Abstract Syntax Tree (AST)** from the token stream. This tree represents the hierarchical syntactic structure of the program.
- 🔹 **Standardizer**: Transforms the AST into a **Standardized AST (SAST)** to simplify interpretation by the CSE machine.
- 🔹 **CSE Machine**: Executes the standardized AST using a **Control Stack Environment (CSE)** model that manages function calls, scopes, and bindings.

---

## ⚙️ Setup Instructions

1. Clone this repository:

   git clone https://github.com/your-repo/project_rpal.git
   cd project_rpal

2. Ensure Python is installed.
   You can download it from [python.org](https://www.python.org/downloads/).

3. No external dependencies are required — only Python's built-in libraries are used.

---

## 📁 File Structure

```
project_rpal/
├── myrpal.py            # Main interpreter script
├── Makefile             # Makefile for simplified execution
├── input.txt            # Example input file
└── inputs/              # Directory containing sample test files
    ├── t1.txt
    ├── t2.txt
    └── ...
```

---

## 🚀 Usage with Makefile

The provided `Makefile` allows you to run the interpreter easily.

### ▶️ Run and Print Final Output

make run file=path/to/your/input.txt

**Example:**

make run file=inputs/t1.txt

### 🌲 Print Abstract Syntax Tree (AST)

make ast file=path/to/your/input.txt

### 🌳 Print Standardized Abstract Syntax Tree (SAST)

make sast file=path/to/your/input.txt

### 🧹 Clean Cached Files

Remove all `__pycache__` directories and Python cache files:

make clean

---

## 🐍 Usage with Python Directly

Alternatively, you can run the interpreter directly with Python:

### ▶️ Run and Print Final Output

python myrpal.py path/to/your/input.txt

### 🌲 Print Abstract Syntax Tree (AST)

python myrpal.py path/to/your/input.txt -ast

### 🌳 Print Standardized AST (SAST)

python myrpal.py path/to/your/input.txt -sast


> **Note:** On some systems, you may need to use `python3` instead of `python`.

---

## ❗ Troubleshooting

### ❌ Python Not Found

Make sure Python is properly installed and added to your system’s PATH.
If you're using Linux or macOS, use:

python3 myrpal.py ...


### ❌ File Not Found

Ensure the file path is correct. Check that:

* The file exists.
* The relative/absolute path is accurate.


## 🙋 Need Help?

If you face any issues or have questions, feel free to contact:

* 📧 Pavan – [pavan.22@cse.mrt.ac.lk]
* 📧 Janidu – [janidu.22@cse.mrt.ac.lk]

For detailed execution steps, see [`Instructions_to_RUN.md`]
