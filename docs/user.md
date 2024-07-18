# compareBoolean

This function uses [SymPy](https://docs.sympy.org/latest/index.html) to test two Boolean expressions for equivalence.
Expressions are considered equal if they result in the same truth table. 

## Syntax

The current syntax expected by this function is based on the bitwise Boolean syntax used in C, Matlab and many other programming languages.
  
|Operator|Meaning  |LaTeX         |
|--------|---------|--------------|
|`A \| B`|`A OR B` |$A + B$       |
|`A & B` |`A AND B`|$A \cdot B$   |
|`A ^ B` |`A XOR B`|$A \oplus B$  |
|`~A`    |`NOT A`  |$\overline{A}$|

The order of precedence is as follows:

1. NOT
2. AND
3. OR/XOR

Brackets can be used to group terms and specify the order of evaluation.
For example, `A & B | C & D` is interpreted as `(A & B) | (C & D)`.

## Inputs

### Optional parameters

There is currently one optional parameter that can be set: `enforce_expression_equality`.

### `enforce_expression_equality`
If this Boolean parameter is true, the response and the answer must be strictly equal, i.e in the same form.
