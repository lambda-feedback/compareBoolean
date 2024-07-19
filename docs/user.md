# compareBoolean

This function uses [SymPy](https://docs.sympy.org/latest/index.html) to test two Boolean expressions for equivalence.
Expressions are considered equal if they result in the same truth table.
  
When answering questions on Booleans, it is easy for students to come up with equivalent expressions but in a different form (e.g. 
if using a Karnaugh map versus by inspection). compareBoolean aims to alleviate some of the frustration that may arise by accepting
any response that is equivalent to the correct answer. 

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

## Examples

The function can understand a wide variety of complex boolean expressions. Here are some examples to illustrate its capabilities.
Each pair of expressions is equivalent, and would be marked as "correct" by compareBoolean.

|Response|Answer |Comments|
|--------|-------|--------|
|`x & y` |`y & x`|A trivial example, but probably the most common way student responses will differ from the answer|
|`(x & ~y) \| (y & ~z)` | `x ^ y` | Both expressions are equivalent to a logical exclusive or. |
|`~(~x & ~y)`|`x \| y`|In this example de Morgan's laws have been used to find an equivalent representation of the OR operator.|

## Inputs

### Optional parameters

There is currently one optional parameter that can be set: `enforce_expression_equality`.

### `enforce_expression_equality`
If this Boolean parameter is true, the response and the answer must be strictly equal, i.e in the same form.
