# DCOMP320 – Stack Implementation

## Purpose
Evaluate arithmetic expressions in `input.txt` using two stacks, and save results in `output.txt`, preserving separator lines.

## Run
1. Install Python 3.10 or later. No third-party packages required.
2. Put `main.py` and `input.txt` in the same folder.
3. Open a terminal in this folder and run `python main.py` (Windows may use `py main.py`).
4. Open `output.txt` to view results.

## Input format
One expression per line. Separator lines consist of at least three hyphens (`-----`). Supported: `+`, `-`, `*`, `/`, parentheses, integers and decimals, and negative numeric literals. Whitespace is optional.

## Output format
Each expression is replaced with its calculated result, while separator lines and blank lines remain in place. Invalid expressions produce an `ERROR:` line so processing continues.

## Implementation
The `Stack` class defines `push`, `pop`, `peek`, `is_empty` and `__len__`. The evaluator uses a values stack and an operators stack; higher-precedence operators are applied first, and parentheses control grouping.

## Assumptions and limitations
- Standard operator precedence and left associativity are used.
- Division by zero and malformed expressions generate an error line.
- Unary minus before parentheses, e.g. `-(2+3)`, is not supported; negative numbers such as `-3` are supported.
- Results use floating-point arithmetic and are formatted to 10 significant digits when not whole numbers.
- Python's `eval()` is not used.

## Example
Input: `3 + 5 * 2` → Output: `13`

## GitHub
Create a repository, push these files, then invite the lecturer as collaborator using the GitHub repository Settings → Collaborators page.
