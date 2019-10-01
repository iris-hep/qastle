# Text AST language

This document describes a language intended to be used in [ServiceX](https://github.com/ssl-hep/ServiceX) and [FuncADL](https://github.com/iris-hep/func_adl) for messages which represent abstract syntax trees (ASTs). The trees specify columnar selections of HEP data.

## Introduction

### Influences

- [`ast` module](https://docs.python.org/3/library/ast.html) in Python
  - FuncADL natively uses ASTs as represented by Python's standard `ast` module, thus it is convenient to base everything at least loosely on Python's ASTs to ease translation. ASTs in Python, however, are extremely dense with information important for a full-featured general programming language but not relevant or useful for our purposes in forming selections of columns.
- [LINQ](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/)
  - FuncADL is roughly based on [LINQtoROOT](https://github.com/gordonwatts/LINQtoROOT), which was based on using LINQ queries on data in ROOT format. LINQ is a query language native to C#. The query operators used in FuncADL (`Select`, `SelectMany`, `Where`, etc.) are those of LINQ, so many of the AST nodes will need to represent these operators.
- [Common Lisp](https://common-lisp.net/)
  - Lisp is a functional programming language with a minimalist syntax definition. We're aiming to use similar syntax because of how sparse it is, so that representations of AST nodes are very lean.

### Guiding principles

- I try not to deviate from the influences listed above without good reason, since they are all already well-established standards. However, with influences from three different languages, it's impossible to adhere to all of them anyway.
- For simplificaion and clarity, anything in Python's `ast` that does not affect static translation into a columnar selction is removed.
- Anything that would result in ambiguity when statically converting to a Python AST with LINQ queries or would prevent this conversion from being possible should be explicitly disallowed for easier debugging.
- I'm trying to keep the syntax both as simple and as uniform as possible while maintaining all necessary functionality. By this, I mean in the sense of the simplicity and uniformity of the definition, which also results in the least complex parsing. Note that this does not result in the most compact AST text possible.

## Language specification

Like Lisp, the language consists solely of s-expressions. All defined s-expressions are listed here, though this specification will be expanded in the future.

- Atomic s-expressions (atoms):
  - Literals:
    - Numeric literals: identical to Python's real number literals
    - String literals: identical to Python's single-quoted or double-quoted strings without prefixes or formatting
  - Identifiers: identical to Python's identifiers (but with a different set of reserved keywords)
    - Variable names: represent a variable defined within the AST in which its name appears
    - Keywords: predefined identifiers which have a special meaning globally and cannot be used as a variable name
      - `True` and `true`: represent a Boolean value of true
      - `False` and `false`: represent a Boolean value of false

- Non-atomic s-expressions:
  - Lists: `(list <item>*)`
  - Attributes: `(attr <object> <attribute>)`
    - `attribute` must be a string literal
  - Unary operators: `(<operator> <operand>)`
    - `operator` must be one of: `+`, `-` (arithmetic); `not` (boolean)
  - Binary operators: `(<operator> <left operand> <right operand>)`
    - `operator` must be one of: `+`, `-`, `*`, `/` (arithmetic); `<`, `<=`, `==`, `!=`, `>`, `>=` (comparison); `and`, `or` (boolean)
  - Lambdas: `(lambda <arguments> <expression>)`
    - `arguments` must be a `list` containing only variable names
  - Select: `(Select <source> <selector>)`
    - `selector` must be a `lambda` with one argument
  - Where: `(Where <source> <predicate>)`
    - `predicate` must be a `lambda` with one argument
  - Count: `(Count <source>)`
