# CYK Parser & Chomsky Normal Form (CNF) Converter

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Topic](https://img.shields.io/badge/Topic-Formal_Languages_&_Automata-orange.svg)]()

A Python implementation of the **Cocke-Younger-Kasami (CYK / CKY)** chart parsing algorithm and an automated **Chomsky Normal Form (CNF)** grammar transformation pipeline. 

The project supports both standard **Context-Free Grammars (CFG)** for formal language membership testing and **Probabilistic Context-Free Grammars (PCFG)** with Viterbi-style maximum probability parsing (**PCKY**).

---

## 📌 Features

- **Chomsky Normal Form (CNF) Conversion**: Full automated pipeline converting arbitrary context-free grammars into equivalent CNF.
- **CYK Membership Parsing**: Bottom-up dynamic programming chart parser with $\mathcal{O}(n^3 \cdot |G|)$ time complexity for string acceptance.
- **Probabilistic CYK (PCKY)**: Computes the most probable derivation tree and associated probability $P(S \Rightarrow^* w)$ for stochastic grammars.
- **Batch Processing**: Supports multi-grammar benchmark files evaluating multiple candidate words per grammar.

---

## 📐 Theoretical Background

### 1. Chomsky Normal Form (CNF)
A context-free grammar is in Chomsky Normal Form if all production rules are of the form:
* $A \to BC$ (where $A, B, C$ are non-terminal symbols, and $B, C \neq S$)
* $A \to a$ (where $a$ is a terminal symbol)
* $S \to \varepsilon$ (optional, if the empty string $\varepsilon$ is in the language)

The conversion engine ([`src/transform_to_cfg.py`](src/transform_to_cfg.py)) executes a 6-step normalization:
1. **$\varepsilon$-Production Elimination**: Identifies nullable non-terminals and expands all non-empty combinations.
2. **Unit Production Elimination**: Replaces chains of unit rules ($A \to B$) with direct derivations.
3. **Mixed Production Replacement**: Replaces terminal symbols appearing alongside non-terminals with dedicated auxiliary variables.
4. **Long Production Binarization**: Decomposes productions with length $> 2$ into binary rule cascades ($A \to B_1 B_2 \dots B_k \implies A \to B_1 C_1, C_1 \to B_2 C_2, \dots$).
5. **Non-Generating Symbol Elimination**: Prunes non-terminals that cannot derive strings composed purely of terminals.
6. **Unreachable Symbol Elimination**: Removes symbols that cannot be reached from the start symbol $S$.

### 2. Standard CYK Dynamic Programming
Given a string $w = w_1 w_2 \dots w_n$:
* **Base Case (substrings of length 1)**:
  $$T[i, i] = \{ A \mid A \to w_i \in G \}$$
* **Inductive Step (substrings of length $l = 2 \dots n$)**:
  $$T[i, j] = \bigcup_{k=i}^{j-1} \{ A \mid A \to BC \in G, \; B \in T[i, k], \; C \in T[k+1, j] \}$$
* **Acceptance Criterion**: $w \in L(G) \iff S \in T[1, n]$.

### 3. Probabilistic CYK (PCKY)
For stochastic rules $A \to BC \; [p]$ and $A \to a \; [p]$:
* **Base Case**:
  $$T[i, i][A] = \max \{ P(A \to w_i) \}$$
* **Inductive Step**:
  $$T[i, j][A] = \max_{\substack{A \to BC \\ k \in [i, j-1]}} \left( P(A \to BC) \times T[i, k][B] \times T[k+1, j][C] \right)$$

---

## 📂 Repository Structure

```directory
cyk-parser-cnf-converter/
├── src/
│   ├── __init__.py          # Package initializer
│   ├── cfg.py               # Context-Free Grammar parser & CYK algorithm
│   ├── pcfg.py              # Probabilistic Context-Free Grammar parser & PCKY algorithm
│   └── transform_to_cfg.py  # Chomsky Normal Form (CNF) transformation pipeline
├── data/
│   ├── input.txt            # Benchmark grammars and test words (standard CFG)
│   └── input_PCKY.txt       # Benchmark grammars with probabilities (PCFG)
├── output/
│   ├── output.txt           # Parsed CNF grammars and membership results
│   └── output_PCKY.txt      # Parsed PCFG results and computed probabilities
├── main.py                  # Batch execution script & file processor
├── .gitignore               # Python environment ignore rules
└── README.md                # Project documentation
```

---

## 🚀 How to Run

### Requirements
Python 3.8+ (no external dependencies required, standard library only).

### Execution

1. Configure the execution mode in [`main.py`](main.py):
   * For **Probabilistic PCFG parsing**: set `usar_pcky = True` (line 11).
   * For **Standard CFG membership parsing**: set `usar_pcky = False` (line 11).

2. Run the main script from the project root:
   ```bash
   python main.py
   ```

3. Inspect generated results in [`output/output.txt`](output/output.txt) or [`output/output_PCKY.txt`](output/output_PCKY.txt).

---

## 📝 Input & Output Format Specifications

### 1. Standard CFG (`data/input.txt`)
Each grammar block is separated by a blank line, followed by the test strings:

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

**Output format (`output/output.txt`)**:
```text
La gramatica ya esta en CNF

Resultados
'ab': True
'abab': True
'ababab': True
'aab': False
'ba': False
```

If the grammar is not in CNF, `transform_to_cfg.py` automatically converts it and displays the resulting rules:
```text
Gramatica no esta en CNF
Gramatica convertida a CNF:
S -> AB | SS
A -> a
C -> b
B -> b
```

### 2. Probabilistic PCFG (`data/input_PCKY.txt`)
Rules include probability weights in square brackets `[prob]`:

```text
S -> AB [0.9] | BC [0.1]
A -> BA [0.5] | a [0.5]
B -> CC [0.7] | b [0.3]
C -> AB [0.6] | a [0.4]
ab
a
```

**Output format (`output/output_PCKY.txt`)**:
```text
La gramatica ya esta en CNF

Resultados
'ab': True (Probabilidad: 0.1350)
'a': False (Probabilidad: 0.0000)
```

---

## 👥 Authors & License

Developed as part of the **Natural Language Processing & Automata Theory** benchmark suite.  
Distributed under the **MIT License**.
