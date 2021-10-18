# qastle (Query AST Language Expressions)

[![Codecov badge](https://codecov.io/gh/iris-hep/qastle/branch/master/graph/badge.svg)](https://codecov.io/gh/iris-hep/qastle)
[![PyPI version](https://badge.fury.io/py/qastle.svg)](https://badge.fury.io/py/qastle)

This document describes a language intended to be used in [ServiceX](https://github.com/ssl-hep/ServiceX) and [func_adl](https://github.com/iris-hep/func_adl) for messages which represent abstract syntax trees (ASTs). The trees specify columnar selections of HEP data.

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

### Syntax

The syntax/grammar definition is discussed [here](doc/ebnf.md). Like Lisp, the language consists solely of s-expressions. S-expressions here represent AST nodes and are either atoms--which include literals and identifiers--or composites of other s-expressions. Literals and names are nearly identical to those in Python. Composites are of the form:

```
(<composite node type> <s-expression 1> <s-expression 2> <s-expression 3> ...)
```

They look like bare lists from Lisp, with the first element describing the type of AST node, and the rest of the elements being the components of the node.

### Semantics

All defined s-expressions are listed here, though this specification will be expanded in the future. The symbol `*` is used as a suffix here in its regex meaning (i.e., zero or more of the object that it follows are expected). Except where there is a restriction explicitly mentioned in the templates below, any type of s-expression can used as an element of a composite s-expression.

- Atomic s-expressions (atoms):
  - Numbers
  - Strings
  - Identifiers
    - Variable names
    - Reserved identifiers: `True`, `False`, and `None`
      - Cannot be used as variable names

- Composite s-expressions:
  - Lists: `(list <item>*)`
  - Dictionary: `(dict <keys> <values>)`
    - `keys` and `values` must each be a `list`
  - Attributes: `(attr <object> <attribute>)`
    - `attribute` must be a string literal
  - Subscripts: `(subscript <object> <subscript>)`
  - Function calls: `(call <function> <argument>*)`
  - Conditionals: `(if <condition> <then> <else>)`
  - Unary operators: `(<operator> <operand>)`
    - `<operator>` must be `not` or `~`
  - Binary operators: `(<operator> <operand> <operand>)`
      - `<operator>` must be one of `+`, `-`, `*`, `/`, `%`, `**`, `//`, `and`, `or`, `&`, `|`, `^`, `<<`, `>>`, `==`, `!=`, `<`, `<=`, `>`, `>=`
  - Lambdas: `(lambda <arguments> <expression>)`
    - `arguments` must be a `list` containing only variable names
  - Where: `(Where <source> <predicate>)`
    - `predicate` must be a `lambda` with one argument
  - Select: `(Select <source> <selector>)`
    - `selector` must be a `lambda` with one argument
  - SelectMany: `(SelectMany <source> <selector>)`
    - `selector` must be a `lambda` with one argument
  - First: `(First <source>)`
  - Last: `(Last <source>)`
  - ElementAt: `(ElementAt <source> <index>)`
    - `index` must be an integer
  - Contains: `(Contains <source> <value>)`
  - Aggregate: `(Aggregate <source> <seed> <func>)`
    - `func` must be a `lambda` with two arguments
  - Count: `(Count <source>)`
  - Max: `(Max <source>)`
  - Min: `(Min <source>)`
  - Sum: `(Sum <source>)`
  - All: `(All <source> <predicate>)`
    - `predicate` must be a `lambda` with one argument
  - Any: `(Any <source> <predicate>)`
    - `predicate` must be a `lambda` with one argument
  - Concat: `(Concat <first> <second>)`
  - Zip: `(Zip <source>)`
  - OrderBy: `(OrderBy <source> <key_selector>)`
    - `key_selector` must be a `lambda` with one argument
  - OrderByDescending: `(OrderByDescending <source> <key_selector>)`
    - `key_selector` must be a `lambda` with one argument
  - Choose: `(Choose <source> <n>)`
    - `n` must be an integer

## Example

The following query for eight columns:

```python
data_column_source.Select("lambda Event: (Event.Electrons.pt(),
                                          Event.Electrons.eta(),
                                          Event.Electrons.phi(),
                                          Event.Electrons.e(),
                                          Event.Muons.pt(),
                                          Event.Muons.eta(),
                                          Event.Muons.phi(),
                                          Event.Muons.e())")
```

becomes

```lisp
(Select data_column_source
        (lambda (list Event)
                (list (call (attr (attr Event 'Electrons') 'pt'))
                      (call (attr (attr Event 'Electrons') 'eta'))
                      (call (attr (attr Event 'Electrons') 'phi'))
                      (call (attr (attr Event 'Electrons') 'e'))
                      (call (attr (attr Event 'Muons') 'pt'))
                      (call (attr (attr Event 'Muons') 'eta'))
                      (call (attr (attr Event 'Muons') 'phi'))
                      (call (attr (attr Event 'Muons') 'e')))))
```

See [this Jupyter notebook](examples/annotated_query_example.ipynb) for a more thorough example.


## Nota bene

The mapping between Python and qastle expressions is not strictly one-to-one. There are some Python nodes with more specific functionality than needed in the textual AST representation. For example, all Python `tuple`s are converted to `(list)`s by qastle.
