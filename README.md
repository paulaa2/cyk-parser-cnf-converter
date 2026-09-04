# CYK Parser & Chomsky Normal Form (CNF) Converter

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Topic](https://img.shields.io/badge/Topic-Formal_Languages_%26_Automata-orange.svg)]()

A Python implementation of the **Cocke-Younger-Kasami (CYK / CKY)** chart parsing algorithm and an automated **Chomsky Normal Form (CNF)** grammar transformation pipeline.

The project supports both standard **Context-Free Grammars (CFG)** for formal language membership testing and **Probabilistic Context-Free Grammars (PCFG)** with Viterbi-style maximum probability parsing (**PCKY**).

---

## Features

- **Chomsky Normal Form (CNF) Conversion**: Full automated pipeline converting arbitrary context-free grammars into equivalent CNF.
- **CYK Membership Parsing**: Bottom-up dynamic programming chart parser with O(n^3 * |G|) time complexity for string acceptance.
- **Probabilistic CYK (PCKY)**: Computes the most probable derivation tree and associated probability for stochastic grammars.
- **Batch Processing**: Supports multi-grammar benchmark files evaluating multiple candidate words per grammar.

---

## Theoretical Background

### 1. Chomsky Normal Form (CNF)
A context-free grammar is in Chomsky Normal Form if all production rules are of the form:
- `A -> BC` (where A, B, C are non-terminals, and B, C are not the start symbol)
- `A -> a` (where `a` is a terminal symbol)
- `S -> ε` (optional, if the empty string is in the language)

The conversion engine ([src/transform_to_cfg.py](src/transform_to_cfg.py)) executes a 6-step normalization:

1. **Epsilon-Production Elimination**: Identifies nullable non-terminals and expands all non-empty combinations.
2. **Unit Production Elimination**: Replaces chains of unit rules (A -> B) with direct derivations.
3. **Mixed Production Replacement**: Replaces terminal symbols appearing alongside non-terminals with dedicated auxiliary variables.
4. **Long Production Binarization**: Decomposes productions with length > 2 into binary rule cascades.
5. **Non-Generating Symbol Elimination**: Prunes non-terminals that cannot derive any terminal string.
6. **Unreachable Symbol Elimination**: Removes symbols unreachable from the start symbol S.

### 2. Standard CYK Dynamic Programming

- **Base Case**: `T[i,i] = { A | A -> w_i in G }`
- **Inductive Step**: `T[i,j] = union over k { A | A -> BC, B in T[i,k], C in T[k+1,j] }`
- **Acceptance**: `w in L(G)` if and only if `S in T[1,n]`

### 3. Probabilistic CYK (PCKY)

- **Base Case**: `T[i,i][A] = max { P(A -> w_i) }`
- **Inductive Step**: `T[i,j][A] = max over (A->BC, k) { P(A->BC) * T[i,k][B] * T[k+1,j][C] }`

---

## Repository Structure

```
cyk-parser-cnf-converter/
├── src/
│   ├── __init__.py          # Package initializer
│   ├── cfg.py               # Context-Free Grammar parser & CYK algorithm
│   ├── pcfg.py              # Probabilistic CFG parser & PCKY algorithm
│   └── transform_to_cfg.py  # CNF transformation pipeline
├── data/
│   ├── input.txt            # Benchmark grammars and test words (standard CFG)
│   └── input_PCKY.txt       # Benchmark grammars with probabilities (PCFG)
├── output/
│   ├── output.txt           # CNF grammars and membership results
│   └── output_PCKY.txt      # PCFG results and computed probabilities
├── main.py                  # Batch execution script & file processor
├── .gitignore
└── README.md
```

---

## How to Run

### Requirements
Python 3.8+ (no external dependencies — standard library only).

### Execution

1. Configure execution mode in [main.py](main.py):
   - For **Probabilistic PCFG parsing**: set `usar_pcky = True` (line 11).
   - For **Standard CFG membership parsing**: set `usar_pcky = False` (line 11).

2. Run the main script from the project root:
   ```bash
   python main.py
   ```

3. Inspect results in `output/output.txt` or `output/output_PCKY.txt`.

---

## Input & Output Format

### 1. Standard CFG (`data/input.txt`)
Grammar blocks separated by blank lines, followed by test strings:

```text
S -> AB | SS
A -> a
B -> b
ab
abab
ababab
aab
ba
```

**Output (`output/output.txt`)**:
```text
La gramatica ya esta en CNF

Resultados
'ab': True
'abab': True
'ababab': True
'aab': False
'ba': False
```

### 2. Probabilistic PCFG (`data/input_PCKY.txt`)
Rules include probability weights in square brackets:

```text
S -> AB [0.9] | BC [0.1]
A -> BA [0.5] | a [0.5]
B -> CC [0.7] | b [0.3]
C -> AB [0.6] | a [0.4]
ab
a
```

**Output (`output/output_PCKY.txt`)**:
```text
'ab': True (Probabilidad: 0.1350)
'a': False (Probabilidad: 0.0000)
```

---

## Authors & License

Developed as part of the **Natural Language Processing & Automata Theory** course.
Distributed under the **MIT License**.
