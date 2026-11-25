# Python Language Reference: Expressions

Source URL: https://docs.python.org/3.13/reference/expressions.html
Reference version: Python 3.13
Licence: Python Software Foundation License Version 2 (https://docs.python.org/3.13/license.html)
Local extraction: CPython 3.13 pydoc_data.topics generated from the official documentation

### TOPIC: atom-identifiers
Identifiers (Names)
*******************

An identifier occurring as an atom is a name.  See section Identifiers
and keywords for lexical definition and section Naming and binding for
documentation of naming and binding.

When the name is bound to an object, evaluation of the atom yields
that object. When a name is not bound, an attempt to evaluate it
raises a "NameError" exception.


Private name mangling
=====================

When an identifier that textually occurs in a class definition begins
with two or more underscore characters and does not end in two or more
underscores, it is considered a *private name* of that class.

See also: The class specifications.

More precisely, private names are transformed to a longer form before
code is generated for them.  If the transformed name is longer than
255 characters, implementation-defined truncation may happen.

The transformation is independent of the syntactical context in which
the identifier is used but only the following private identifiers are
mangled:

* Any name used as the name of a variable that is assigned or read or
  any name of an attribute being accessed.

  The "__name__" attribute of nested functions, classes, and type
  aliases is however not mangled.

* The name of imported modules, e.g., "__spam" in "import __spam". If
  the module is part of a package (i.e., its name contains a dot), the
  name is *not* mangled, e.g., the "__foo" in "import __foo.bar" is
  not mangled.

* The name of an imported member, e.g., "__f" in "from spam import
  __f".

The transformation rule is defined as follows:

* The class name, with leading underscores removed and a single
  leading underscore inserted, is inserted in front of the identifier,
  e.g., the identifier "__spam" occurring in a class named "Foo",
  "_Foo" or "__Foo" is transformed to "_Foo__spam".

* If the class name consists only of underscores, the transformation
  is the identity, e.g., the identifier "__spam" occurring in a class
  named "_" or "__" is left as is.

### TOPIC: atom-literals
Literals
********

Python supports string and bytes literals and various numeric
literals:

   literal ::= stringliteral | bytesliteral
               | integer | floatnumber | imagnumber

Evaluation of a literal yields an object of the given type (string,
bytes, integer, floating-point number, complex number) with the given
value.  The value may be approximated in the case of floating-point
and imaginary (complex) literals.  See section Literals for details.

All literals correspond to immutable data types, and hence the
object’s identity is less important than its value.  Multiple
evaluations of literals with the same value (either the same
occurrence in the program text or a different occurrence) may obtain
the same object or a different object with the same value.

### TOPIC: attribute-references
Attribute references
********************

An attribute reference is a primary followed by a period and a name:

   attributeref ::= primary "." identifier

The primary must evaluate to an object of a type that supports
attribute references, which most objects do.  This object is then
asked to produce the attribute whose name is the identifier. The type
and value produced is determined by the object.  Multiple evaluations
of the same attribute reference may yield different objects.

This production can be customized by overriding the
"__getattribute__()" method or the "__getattr__()" method.  The
"__getattribute__()" method is called first and either returns a value
or raises "AttributeError" if the attribute is not available.

If an "AttributeError" is raised and the object has a "__getattr__()"
method, that method is called as a fallback.

### TOPIC: subscriptions
Subscriptions
*************

The subscription of an instance of a container class will generally
select an element from the container. The subscription of a *generic
class* will generally return a GenericAlias object.

   subscription ::= primary "[" flexible_expression_list "]"

When an object is subscripted, the interpreter will evaluate the
primary and the expression list.

The primary must evaluate to an object that supports subscription. An
object may support subscription through defining one or both of
"__getitem__()" and "__class_getitem__()". When the primary is
subscripted, the evaluated result of the expression list will be
passed to one of these methods. For more details on when
"__class_getitem__" is called instead of "__getitem__", see
__class_getitem__ versus __getitem__.

If the expression list contains at least one comma, or if any of the
expressions are starred, the expression list will evaluate to a
"tuple" containing the items of the expression list. Otherwise, the
expression list will evaluate to the value of the list’s sole member.

Changed in version 3.11: Expressions in an expression list may be
starred. See **PEP 646**.

For built-in objects, there are two types of objects that support
subscription via "__getitem__()":

1. Mappings. If the primary is a *mapping*, the expression list must
   evaluate to an object whose value is one of the keys of the
   mapping, and the subscription selects the value in the mapping that
   corresponds to that key. An example of a builtin mapping class is
   the "dict" class.

2. Sequences. If the primary is a *sequence*, the expression list must
   evaluate to an "int" or a "slice" (as discussed in the following
   section). Examples of builtin sequence classes include the "str",
   "list" and "tuple" classes.

The formal syntax makes no special provision for negative indices in
*sequences*. However, built-in sequences all provide a "__getitem__()"
method that interprets negative indices by adding the length of the
sequence to the index so that, for example, "x[-1]" selects the last
item of "x". The resulting value must be a nonnegative integer less
than the number of items in the sequence, and the subscription selects
the item whose index is that value (counting from zero). Since the
support for negative indices and slicing occurs in the object’s
"__getitem__()" method, subclasses overriding this method will need to
explicitly add that support.

A "string" is a special kind of sequence whose items are *characters*.
A character is not a separate data type but a string of exactly one
character.

### TOPIC: slicings
Slicings
********

A slicing selects a range of items in a sequence object (e.g., a
string, tuple or list).  Slicings may be used as expressions or as
targets in assignment or "del" statements.  The syntax for a slicing:

   slicing      ::= primary "[" slice_list "]"
   slice_list   ::= slice_item ("," slice_item)* [","]
   slice_item   ::= expression | proper_slice
   proper_slice ::= [lower_bound] ":" [upper_bound] [ ":" [stride] ]
   lower_bound  ::= expression
   upper_bound  ::= expression
   stride       ::= expression

There is ambiguity in the formal syntax here: anything that looks like
an expression list also looks like a slice list, so any subscription
can be interpreted as a slicing.  Rather than further complicating the
syntax, this is disambiguated by defining that in this case the
interpretation as a subscription takes priority over the
interpretation as a slicing (this is the case if the slice list
contains no proper slice).

The semantics for a slicing are as follows.  The primary is indexed
(using the same "__getitem__()" method as normal subscription) with a
key that is constructed from the slice list, as follows.  If the slice
list contains at least one comma, the key is a tuple containing the
conversion of the slice items; otherwise, the conversion of the lone
slice item is the key.  The conversion of a slice item that is an
expression is that expression.  The conversion of a proper slice is a
slice object (see section The standard type hierarchy) whose "start",
"stop" and "step" attributes are the values of the expressions given
as lower bound, upper bound and stride, respectively, substituting
"None" for missing expressions.

### TOPIC: calls
Calls
*****

A call calls a callable object (e.g., a *function*) with a possibly
empty series of *arguments*:

   call                 ::= primary "(" [argument_list [","] | comprehension] ")"
   argument_list        ::= positional_arguments ["," starred_and_keywords]
                            ["," keywords_arguments]
                            | starred_and_keywords ["," keywords_arguments]
                            | keywords_arguments
   positional_arguments ::= positional_item ("," positional_item)*
   positional_item      ::= assignment_expression | "*" expression
   starred_and_keywords ::= ("*" expression | keyword_item)
                            ("," "*" expression | "," keyword_item)*
   keywords_arguments   ::= (keyword_item | "**" expression)
                            ("," keyword_item | "," "**" expression)*
   keyword_item         ::= identifier "=" expression

An optional trailing comma may be present after the positional and
keyword arguments but does not affect the semantics.

The primary must evaluate to a callable object (user-defined
functions, built-in functions, methods of built-in objects, class
objects, methods of class instances, and all objects having a
"__call__()" method are callable).  All argument expressions are
evaluated before the call is attempted.  Please refer to section
Function definitions for the syntax of formal *parameter* lists.

If keyword arguments are present, they are first converted to
positional arguments, as follows.  First, a list of unfilled slots is
created for the formal parameters.  If there are N positional
arguments, they are placed in the first N slots.  Next, for each
keyword argument, the identifier is used to determine the
corresponding slot (if the identifier is the same as the first formal
parameter name, the first slot is used, and so on).  If the slot is
already filled, a "TypeError" exception is raised. Otherwise, the
argument is placed in the slot, filling it (even if the expression is
"None", it fills the slot).  When all arguments have been processed,
the slots that are still unfilled are filled with the corresponding
default value from the function definition.  (Default values are
calculated, once, when the function is defined; thus, a mutable object
such as a list or dictionary used as default value will be shared by
all calls that don’t specify an argument value for the corresponding
slot; this should usually be avoided.)  If there are any unfilled
slots for which no default value is specified, a "TypeError" exception
is raised.  Otherwise, the list of filled slots is used as the
argument list for the call.

**CPython implementation detail:** An implementation may provide
built-in functions whose positional parameters do not have names, even
if they are ‘named’ for the purpose of documentation, and which
therefore cannot be supplied by keyword.  In CPython, this is the case
for functions implemented in C that use "PyArg_ParseTuple()" to parse
their arguments.

If there are more positional arguments than there are formal parameter
slots, a "TypeError" exception is raised, unless a formal parameter
using the syntax "*identifier" is present; in this case, that formal
parameter receives a tuple containing the excess positional arguments
(or an empty tuple if there were no excess positional arguments).

If any keyword argument does not correspond to a formal parameter
name, a "TypeError" exception is raised, unless a formal parameter
using the syntax "**identifier" is present; in this case, that formal
parameter receives a dictionary containing the excess keyword
arguments (using the keywords as keys and the argument values as
corresponding values), or a (new) empty dictionary if there were no
excess keyword arguments.

If the syntax "*expression" appears in the function call, "expression"
must evaluate to an *iterable*.  Elements from these iterables are
treated as if they were additional positional arguments.  For the call
"f(x1, x2, *y, x3, x4)", if *y* evaluates to a sequence *y1*, …, *yM*,
this is equivalent to a call with M+4 positional arguments *x1*, *x2*,
*y1*, …, *yM*, *x3*, *x4*.

A consequence of this is that although the "*expression" syntax may
appear *after* explicit keyword arguments, it is processed *before*
the keyword arguments (and any "**expression" arguments – see below).
So:

   >>> def f(a, b):
   ...     print(a, b)
   ...
   >>> f(b=1, *(2,))
   2 1
   >>> f(a=1, *(2,))
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: f() got multiple values for keyword argument 'a'
   >>> f(1, *(2,))
   1 2

It is unusual for both keyword arguments and the "*expression" syntax
to be used in the same call, so in practice this confusion does not
often arise.

If the syntax "**expression" appears in the function call,
"expression" must evaluate to a *mapping*, the contents of which are
treated as additional keyword arguments. If a parameter matching a key
has already been given a value (by an explicit keyword argument, or
from another unpacking), a "TypeError" exception is raised.

When "**expression" is used, each key in this mapping must be a
string. Each value from the mapping is assigned to the first formal
parameter eligible for keyword assignment whose name is equal to the
key. A key need not be a Python identifier (e.g. ""max-temp °F"" is
acceptable, although it will not match any formal parameter that could
be declared). If there is no match to a formal parameter the key-value
pair is collected by the "**" parameter, if there is one, or if there
is not, a "TypeError" exception is raised.

Formal parameters using the syntax "*identifier" or "**identifier"
cannot be used as positional argument slots or as keyword argument
names.

Changed in version 3.5: Function calls accept any number of "*" and
"**" unpackings, positional arguments may follow iterable unpackings
("*"), and keyword arguments may follow dictionary unpackings ("**").
Originally proposed by **PEP 448**.

A call always returns some value, possibly "None", unless it raises an
exception.  How this value is computed depends on the type of the
callable object.

If it is—

a user-defined function:
   The code block for the function is executed, passing it the
   argument list.  The first thing the code block will do is bind the
   formal parameters to the arguments; this is described in section
   Function definitions.  When the code block executes a "return"
   statement, this specifies the return value of the function call.
   If execution reaches the end of the code block without executing a
   "return" statement, the return value is "None".

a built-in function or method:
   The result is up to the interpreter; see Built-in Functions for the
   descriptions of built-in functions and methods.

a class object:
   A new instance of that class is returned.

a class instance method:
   The corresponding user-defined function is called, with an argument
   list that is one longer than the argument list of the call: the
   instance becomes the first argument.

a class instance:
   The class must define a "__call__()" method; the effect is then the
   same as if that method was called.

### TOPIC: await
Await expression
****************

Suspend the execution of *coroutine* on an *awaitable* object. Can
only be used inside a *coroutine function*.

   await_expr ::= "await" primary

Added in version 3.5.

### TOPIC: power
The power operator
******************

The power operator binds more tightly than unary operators on its
left; it binds less tightly than unary operators on its right.  The
syntax is:

   power ::= (await_expr | primary) ["**" u_expr]

Thus, in an unparenthesized sequence of power and unary operators, the
operators are evaluated from right to left (this does not constrain
the evaluation order for the operands): "-1**2" results in "-1".

The power operator has the same semantics as the built-in "pow()"
function, when called with two arguments: it yields its left argument
raised to the power of its right argument.  The numeric arguments are
first converted to a common type, and the result is of that type.

For int operands, the result has the same type as the operands unless
the second argument is negative; in that case, all arguments are
converted to float and a float result is delivered. For example,
"10**2" returns "100", but "10**-2" returns "0.01".

Raising "0.0" to a negative power results in a "ZeroDivisionError".
Raising a negative number to a fractional power results in a "complex"
number. (In earlier versions it raised a "ValueError".)

This operation can be customized using the special "__pow__()" and
"__rpow__()" methods.

### TOPIC: unary
Unary arithmetic and bitwise operations
***************************************

All unary arithmetic and bitwise operations have the same priority:

   u_expr ::= power | "-" u_expr | "+" u_expr | "~" u_expr

The unary "-" (minus) operator yields the negation of its numeric
argument; the operation can be overridden with the "__neg__()" special
method.

The unary "+" (plus) operator yields its numeric argument unchanged;
the operation can be overridden with the "__pos__()" special method.

The unary "~" (invert) operator yields the bitwise inversion of its
integer argument.  The bitwise inversion of "x" is defined as
"-(x+1)".  It only applies to integral numbers or to custom objects
that override the "__invert__()" special method.

In all three cases, if the argument does not have the proper type, a
"TypeError" exception is raised.

### TOPIC: binary
Binary arithmetic operations
****************************

The binary arithmetic operations have the conventional priority
levels.  Note that some of these operations also apply to certain non-
numeric types.  Apart from the power operator, there are only two
levels, one for multiplicative operators and one for additive
operators:

   m_expr ::= u_expr | m_expr "*" u_expr | m_expr "@" m_expr |
              m_expr "//" u_expr | m_expr "/" u_expr |
              m_expr "%" u_expr
   a_expr ::= m_expr | a_expr "+" m_expr | a_expr "-" m_expr

The "*" (multiplication) operator yields the product of its arguments.
The arguments must either both be numbers, or one argument must be an
integer and the other must be a sequence. In the former case, the
numbers are converted to a common type and then multiplied together.
In the latter case, sequence repetition is performed; a negative
repetition factor yields an empty sequence.

This operation can be customized using the special "__mul__()" and
"__rmul__()" methods.

The "@" (at) operator is intended to be used for matrix
multiplication.  No builtin Python types implement this operator.

This operation can be customized using the special "__matmul__()" and
"__rmatmul__()" methods.

Added in version 3.5.

The "/" (division) and "//" (floor division) operators yield the
quotient of their arguments.  The numeric arguments are first
converted to a common type. Division of integers yields a float, while
floor division of integers results in an integer; the result is that
of mathematical division with the ‘floor’ function applied to the
result.  Division by zero raises the "ZeroDivisionError" exception.

The division operation can be customized using the special
"__truediv__()" and "__rtruediv__()" methods. The floor division
operation can be customized using the special "__floordiv__()" and
"__rfloordiv__()" methods.

The "%" (modulo) operator yields the remainder from the division of
the first argument by the second.  The numeric arguments are first
converted to a common type.  A zero right argument raises the
"ZeroDivisionError" exception.  The arguments may be floating-point
numbers, e.g., "3.14%0.7" equals "0.34" (since "3.14" equals "4*0.7 +
0.34".)  The modulo operator always yields a result with the same sign
as its second operand (or zero); the absolute value of the result is
strictly smaller than the absolute value of the second operand [1].

The floor division and modulo operators are connected by the following
identity: "x == (x//y)*y + (x%y)".  Floor division and modulo are also
connected with the built-in function "divmod()": "divmod(x, y) ==
(x//y, x%y)". [2].

In addition to performing the modulo operation on numbers, the "%"
operator is also overloaded by string objects to perform old-style
string formatting (also known as interpolation).  The syntax for
string formatting is described in the Python Library Reference,
section printf-style String Formatting.

The *modulo* operation can be customized using the special "__mod__()"
and "__rmod__()" methods.

The floor division operator, the modulo operator, and the "divmod()"
function are not defined for complex numbers.  Instead, convert to a
floating-point number using the "abs()" function if appropriate.

The "+" (addition) operator yields the sum of its arguments.  The
arguments must either both be numbers or both be sequences of the same
type.  In the former case, the numbers are converted to a common type
and then added together. In the latter case, the sequences are
concatenated.

This operation can be customized using the special "__add__()" and
"__radd__()" methods.

The "-" (subtraction) operator yields the difference of its arguments.
The numeric arguments are first converted to a common type.

This operation can be customized using the special "__sub__()" and
"__rsub__()" methods.

### TOPIC: shifting
Shifting operations
*******************

The shifting operations have lower priority than the arithmetic
operations:

   shift_expr ::= a_expr | shift_expr ("<<" | ">>") a_expr

These operators accept integers as arguments.  They shift the first
argument to the left or right by the number of bits given by the
second argument.

The left shift operation can be customized using the special
"__lshift__()" and "__rlshift__()" methods. The right shift operation
can be customized using the special "__rshift__()" and "__rrshift__()"
methods.

A right shift by *n* bits is defined as floor division by "pow(2,n)".
A left shift by *n* bits is defined as multiplication with "pow(2,n)".

### TOPIC: bitwise
Binary bitwise operations
*************************

Each of the three bitwise operations has a different priority level:

   and_expr ::= shift_expr | and_expr "&" shift_expr
   xor_expr ::= and_expr | xor_expr "^" and_expr
   or_expr  ::= xor_expr | or_expr "|" xor_expr

The "&" operator yields the bitwise AND of its arguments, which must
be integers or one of them must be a custom object overriding
"__and__()" or "__rand__()" special methods.

The "^" operator yields the bitwise XOR (exclusive OR) of its
arguments, which must be integers or one of them must be a custom
object overriding "__xor__()" or "__rxor__()" special methods.

The "|" operator yields the bitwise (inclusive) OR of its arguments,
which must be integers or one of them must be a custom object
overriding "__or__()" or "__ror__()" special methods.

### TOPIC: comparisons
Comparisons
***********

Unlike C, all comparison operations in Python have the same priority,
which is lower than that of any arithmetic, shifting or bitwise
operation.  Also unlike C, expressions like "a < b < c" have the
interpretation that is conventional in mathematics:

   comparison    ::= or_expr (comp_operator or_expr)*
   comp_operator ::= "<" | ">" | "==" | ">=" | "<=" | "!="
                     | "is" ["not"] | ["not"] "in"

Comparisons yield boolean values: "True" or "False". Custom *rich
comparison methods* may return non-boolean values. In this case Python
will call "bool()" on such value in boolean contexts.

Comparisons can be chained arbitrarily, e.g., "x < y <= z" is
equivalent to "x < y and y <= z", except that "y" is evaluated only
once (but in both cases "z" is not evaluated at all when "x < y" is
found to be false).

Formally, if *a*, *b*, *c*, …, *y*, *z* are expressions and *op1*,
*op2*, …, *opN* are comparison operators, then "a op1 b op2 c ... y
opN z" is equivalent to "a op1 b and b op2 c and ... y opN z", except
that each expression is evaluated at most once.

Note that "a op1 b op2 c" doesn’t imply any kind of comparison between
*a* and *c*, so that, e.g., "x < y > z" is perfectly legal (though
perhaps not pretty).


Value comparisons
=================

The operators "<", ">", "==", ">=", "<=", and "!=" compare the values
of two objects.  The objects do not need to have the same type.

Chapter Objects, values and types states that objects have a value (in
addition to type and identity).  The value of an object is a rather
abstract notion in Python: For example, there is no canonical access
method for an object’s value.  Also, there is no requirement that the
value of an object should be constructed in a particular way, e.g.
comprised of all its data attributes. Comparison operators implement a
particular notion of what the value of an object is.  One can think of
them as defining the value of an object indirectly, by means of their
comparison implementation.

Because all types are (direct or indirect) subtypes of "object", they
inherit the default comparison behavior from "object".  Types can
customize their comparison behavior by implementing *rich comparison
methods* like "__lt__()", described in Basic customization.

The default behavior for equality comparison ("==" and "!=") is based
on the identity of the objects.  Hence, equality comparison of
instances with the same identity results in equality, and equality
comparison of instances with different identities results in
inequality.  A motivation for this default behavior is the desire that
all objects should be reflexive (i.e. "x is y" implies "x == y").

A default order comparison ("<", ">", "<=", and ">=") is not provided;
an attempt raises "TypeError".  A motivation for this default behavior
is the lack of a similar invariant as for equality.

The behavior of the default equality comparison, that instances with
different identities are always unequal, may be in contrast to what
types will need that have a sensible definition of object value and
value-based equality.  Such types will need to customize their
comparison behavior, and in fact, a number of built-in types have done
that.

The following list describes the comparison behavior of the most
important built-in types.

* Numbers of built-in numeric types (Numeric Types — int, float,
  complex) and of the standard library types "fractions.Fraction" and
  "decimal.Decimal" can be compared within and across their types,
  with the restriction that complex numbers do not support order
  comparison.  Within the limits of the types involved, they compare
  mathematically (algorithmically) correct without loss of precision.

  The not-a-number values "float('NaN')" and "decimal.Decimal('NaN')"
  are special.  Any ordered comparison of a number to a not-a-number
  value is false. A counter-intuitive implication is that not-a-number
  values are not equal to themselves.  For example, if "x =
  float('NaN')", "3 < x", "x < 3" and "x == x" are all false, while "x
  != x" is true.  This behavior is compliant with IEEE 754.

* "None" and "NotImplemented" are singletons.  **PEP 8** advises that
  comparisons for singletons should always be done with "is" or "is
  not", never the equality operators.

* Binary sequences (instances of "bytes" or "bytearray") can be
  compared within and across their types.  They compare
  lexicographically using the numeric values of their elements.

* Strings (instances of "str") compare lexicographically using the
  numerical Unicode code points (the result of the built-in function
  "ord()") of their characters. [3]

  Strings and binary sequences cannot be directly compared.

* Sequences (instances of "tuple", "list", or "range") can be compared
  only within each of their types, with the restriction that ranges do
  not support order comparison.  Equality comparison across these
  types results in inequality, and ordering comparison across these
  types raises "TypeError".

  Sequences compare lexicographically using comparison of
  corresponding elements.  The built-in containers typically assume
  identical objects are equal to themselves.  That lets them bypass
  equality tests for identical objects to improve performance and to
  maintain their internal invariants.

  Lexicographical comparison between built-in collections works as
  follows:

  * For two collections to compare equal, they must be of the same
    type, have the same length, and each pair of corresponding
    elements must compare equal (for example, "[1,2] == (1,2)" is
    false because the type is not the same).

  * Collections that support order comparison are ordered the same as
    their first unequal elements (for example, "[1,2,x] <= [1,2,y]"
    has the same value as "x <= y").  If a corresponding element does
    not exist, the shorter collection is ordered first (for example,
    "[1,2] < [1,2,3]" is true).

* Mappings (instances of "dict") compare equal if and only if they
  have equal "(key, value)" pairs. Equality comparison of the keys and
  values enforces reflexivity.

  Order comparisons ("<", ">", "<=", and ">=") raise "TypeError".

* Sets (instances of "set" or "frozenset") can be compared within and
  across their types.

  They define order comparison operators to mean subset and superset
  tests.  Those relations do not define total orderings (for example,
  the two sets "{1,2}" and "{2,3}" are not equal, nor subsets of one
  another, nor supersets of one another).  Accordingly, sets are not
  appropriate arguments for functions which depend on total ordering
  (for example, "min()", "max()", and "sorted()" produce undefined
  results given a list of sets as inputs).

  Comparison of sets enforces reflexivity of its elements.

* Most other built-in types have no comparison methods implemented, so
  they inherit the default comparison behavior.

User-defined classes that customize their comparison behavior should
follow some consistency rules, if possible:

* Equality comparison should be reflexive. In other words, identical
  objects should compare equal:

     "x is y" implies "x == y"

* Comparison should be symmetric. In other words, the following
  expressions should have the same result:

     "x == y" and "y == x"

     "x != y" and "y != x"

     "x < y" and "y > x"

     "x <= y" and "y >= x"

* Comparison should be transitive. The following (non-exhaustive)
  examples illustrate that:

     "x > y and y > z" implies "x > z"

     "x < y and y <= z" implies "x < z"

* Inverse comparison should result in the boolean negation. In other
  words, the following expressions should have the same result:

     "x == y" and "not x != y"

     "x < y" and "not x >= y" (for total ordering)

     "x > y" and "not x <= y" (for total ordering)

  The last two expressions apply to totally ordered collections (e.g.
  to sequences, but not to sets or mappings). See also the
  "total_ordering()" decorator.

* The "hash()" result should be consistent with equality. Objects that
  are equal should either have the same hash value, or be marked as
  unhashable.

Python does not enforce these consistency rules. In fact, the
not-a-number values are an example for not following these rules.


Membership test operations
==========================

The operators "in" and "not in" test for membership.  "x in s"
evaluates to "True" if *x* is a member of *s*, and "False" otherwise.
"x not in s" returns the negation of "x in s".  All built-in sequences
and set types support this as well as dictionary, for which "in" tests
whether the dictionary has a given key. For container types such as
list, tuple, set, frozenset, dict, or collections.deque, the
expression "x in y" is equivalent to "any(x is e or x == e for e in
y)".

For the string and bytes types, "x in y" is "True" if and only if *x*
is a substring of *y*.  An equivalent test is "y.find(x) != -1".
Empty strings are always considered to be a substring of any other
string, so """ in "abc"" will return "True".

For user-defined classes which define the "__contains__()" method, "x
in y" returns "True" if "y.__contains__(x)" returns a true value, and
"False" otherwise.

For user-defined classes which do not define "__contains__()" but do
define "__iter__()", "x in y" is "True" if some value "z", for which
the expression "x is z or x == z" is true, is produced while iterating
over "y". If an exception is raised during the iteration, it is as if
"in" raised that exception.

Lastly, the old-style iteration protocol is tried: if a class defines
"__getitem__()", "x in y" is "True" if and only if there is a non-
negative integer index *i* such that "x is y[i] or x == y[i]", and no
lower integer index raises the "IndexError" exception.  (If any other
exception is raised, it is as if "in" raised that exception).

The operator "not in" is defined to have the inverse truth value of
"in".


Identity comparisons
====================

The operators "is" and "is not" test for an object’s identity: "x is
y" is true if and only if *x* and *y* are the same object.  An
Object’s identity is determined using the "id()" function.  "x is not
y" yields the inverse truth value. [4]

### TOPIC: booleans
Boolean operations
******************

   or_test  ::= and_test | or_test "or" and_test
   and_test ::= not_test | and_test "and" not_test
   not_test ::= comparison | "not" not_test

In the context of Boolean operations, and also when expressions are
used by control flow statements, the following values are interpreted
as false: "False", "None", numeric zero of all types, and empty
strings and containers (including strings, tuples, lists,
dictionaries, sets and frozensets).  All other values are interpreted
as true.  User-defined objects can customize their truth value by
providing a "__bool__()" method.

The operator "not" yields "True" if its argument is false, "False"
otherwise.

The expression "x and y" first evaluates *x*; if *x* is false, its
value is returned; otherwise, *y* is evaluated and the resulting value
is returned.

The expression "x or y" first evaluates *x*; if *x* is true, its value
is returned; otherwise, *y* is evaluated and the resulting value is
returned.

Note that neither "and" nor "or" restrict the value and type they
return to "False" and "True", but rather return the last evaluated
argument.  This is sometimes useful, e.g., if "s" is a string that
should be replaced by a default value if it is empty, the expression
"s or 'foo'" yields the desired value.  Because "not" has to create a
new value, it returns a boolean value regardless of the type of its
argument (for example, "not 'foo'" produces "False" rather than "''".)

### TOPIC: assignment-expressions
Assignment expressions
**********************

   assignment_expression ::= [identifier ":="] expression

An assignment expression (sometimes also called a “named expression”
or “walrus”) assigns an "expression" to an "identifier", while also
returning the value of the "expression".

One common use case is when handling matched regular expressions:

   if matching := pattern.search(data):
       do_something(matching)

Or, when processing a file stream in chunks:

   while chunk := file.read(9000):
       process(chunk)

Assignment expressions must be surrounded by parentheses when used as
expression statements and when used as sub-expressions in slicing,
conditional, lambda, keyword-argument, and comprehension-if
expressions and in "assert", "with", and "assignment" statements. In
all other places where they can be used, parentheses are not required,
including in "if" and "while" statements.

Added in version 3.8: See **PEP 572** for more details about
assignment expressions.

### TOPIC: lambda
Lambdas
*******

   lambda_expr ::= "lambda" [parameter_list] ":" expression

Lambda expressions (sometimes called lambda forms) are used to create
anonymous functions. The expression "lambda parameters: expression"
yields a function object.  The unnamed object behaves like a function
object defined with:

   def <lambda>(parameters):
       return expression

See section Function definitions for the syntax of parameter lists.
Note that functions created with lambda expressions cannot contain
statements or annotations.

### TOPIC: exprlists
Expression lists
****************

   starred_expression       ::= ["*"] or_expr
   flexible_expression      ::= assignment_expression | starred_expression
   flexible_expression_list ::= flexible_expression ("," flexible_expression)* [","]
   starred_expression_list  ::= starred_expression ("," starred_expression)* [","]
   expression_list          ::= expression ("," expression)* [","]
   yield_list               ::= expression_list | starred_expression "," [starred_expression_list]

Except when part of a list or set display, an expression list
containing at least one comma yields a tuple.  The length of the tuple
is the number of expressions in the list.  The expressions are
evaluated from left to right.

An asterisk "*" denotes *iterable unpacking*.  Its operand must be an
*iterable*.  The iterable is expanded into a sequence of items, which
are included in the new tuple, list, or set, at the site of the
unpacking.

Added in version 3.5: Iterable unpacking in expression lists,
originally proposed by **PEP 448**.

Added in version 3.11: Any item in an expression list may be starred.
See **PEP 646**.

A trailing comma is required only to create a one-item tuple, such as
"1,"; it is optional in all other cases. A single expression without a
trailing comma doesn’t create a tuple, but rather yields the value of
that expression. (To create an empty tuple, use an empty pair of
parentheses: "()".)

### TOPIC: dict
Dictionary displays
*******************

A dictionary display is a possibly empty series of dict items
(key/value pairs) enclosed in curly braces:

   dict_display       ::= "{" [dict_item_list | dict_comprehension] "}"
   dict_item_list     ::= dict_item ("," dict_item)* [","]
   dict_item          ::= expression ":" expression | "**" or_expr
   dict_comprehension ::= expression ":" expression comp_for

A dictionary display yields a new dictionary object.

If a comma-separated sequence of dict items is given, they are
evaluated from left to right to define the entries of the dictionary:
each key object is used as a key into the dictionary to store the
corresponding value.  This means that you can specify the same key
multiple times in the dict item list, and the final dictionary’s value
for that key will be the last one given.

A double asterisk "**" denotes *dictionary unpacking*. Its operand
must be a *mapping*.  Each mapping item is added to the new
dictionary.  Later values replace values already set by earlier dict
items and earlier dictionary unpackings.

Added in version 3.5: Unpacking into dictionary displays, originally
proposed by **PEP 448**.

A dict comprehension, in contrast to list and set comprehensions,
needs two expressions separated with a colon followed by the usual
“for” and “if” clauses. When the comprehension is run, the resulting
key and value elements are inserted in the new dictionary in the order
they are produced.

Restrictions on the types of the key values are listed earlier in
section The standard type hierarchy.  (To summarize, the key type
should be *hashable*, which excludes all mutable objects.)  Clashes
between duplicate keys are not detected; the last value (textually
rightmost in the display) stored for a given key value prevails.

Changed in version 3.8: Prior to Python 3.8, in dict comprehensions,
the evaluation order of key and value was not well-defined.  In
CPython, the value was evaluated before the key.  Starting with 3.8,
the key is evaluated before the value, as proposed by **PEP 572**.

### TOPIC: lists
List displays
*************

A list display is a possibly empty series of expressions enclosed in
square brackets:

   list_display ::= "[" [flexible_expression_list | comprehension] "]"

A list display yields a new list object, the contents being specified
by either a list of expressions or a comprehension.  When a comma-
separated list of expressions is supplied, its elements are evaluated
from left to right and placed into the list object in that order.
When a comprehension is supplied, the list is constructed from the
elements resulting from the comprehension.

### TOPIC: in
Membership test operations
**************************

The operators "in" and "not in" test for membership.  "x in s"
evaluates to "True" if *x* is a member of *s*, and "False" otherwise.
"x not in s" returns the negation of "x in s".  All built-in sequences
and set types support this as well as dictionary, for which "in" tests
whether the dictionary has a given key. For container types such as
list, tuple, set, frozenset, dict, or collections.deque, the
expression "x in y" is equivalent to "any(x is e or x == e for e in
y)".

For the string and bytes types, "x in y" is "True" if and only if *x*
is a substring of *y*.  An equivalent test is "y.find(x) != -1".
Empty strings are always considered to be a substring of any other
string, so """ in "abc"" will return "True".

For user-defined classes which define the "__contains__()" method, "x
in y" returns "True" if "y.__contains__(x)" returns a true value, and
"False" otherwise.

For user-defined classes which do not define "__contains__()" but do
define "__iter__()", "x in y" is "True" if some value "z", for which
the expression "x is z or x == z" is true, is produced while iterating
over "y". If an exception is raised during the iteration, it is as if
"in" raised that exception.

Lastly, the old-style iteration protocol is tried: if a class defines
"__getitem__()", "x in y" is "True" if and only if there is a non-
negative integer index *i* such that "x is y[i] or x == y[i]", and no
lower integer index raises the "IndexError" exception.  (If any other
exception is raised, it is as if "in" raised that exception).

The operator "not in" is defined to have the inverse truth value of
"in".

### TOPIC: conversions
Arithmetic conversions
**********************

When a description of an arithmetic operator below uses the phrase
“the numeric arguments are converted to a common type”, this means
that the operator implementation for built-in types works as follows:

* If either argument is a complex number, the other is converted to
  complex;

* otherwise, if either argument is a floating-point number, the other
  is converted to floating point;

* otherwise, both must be integers and no conversion is necessary.

Some additional rules apply for certain operators (e.g., a string as a
left argument to the ‘%’ operator).  Extensions must define their own
conversion behavior.

### TOPIC: operator-summary
Operator precedence
*******************

The following table summarizes the operator precedence in Python, from
highest precedence (most binding) to lowest precedence (least
binding).  Operators in the same box have the same precedence.  Unless
the syntax is explicitly given, operators are binary.  Operators in
the same box group left to right (except for exponentiation and
conditional expressions, which group from right to left).

Note that comparisons, membership tests, and identity tests, all have
the same precedence and have a left-to-right chaining feature as
described in the Comparisons section.

+-------------------------------------------------+---------------------------------------+
| Operator                                        | Description                           |
|=================================================|=======================================|
| "(expressions...)",  "[expressions...]", "{key: | Binding or parenthesized expression,  |
| value...}", "{expressions...}"                  | list display, dictionary display, set |
|                                                 | display                               |
+-------------------------------------------------+---------------------------------------+
| "x[index]", "x[index:index]",                   | Subscription, slicing, call,          |
| "x(arguments...)", "x.attribute"                | attribute reference                   |
+-------------------------------------------------+---------------------------------------+
| "await x"                                       | Await expression                      |
+-------------------------------------------------+---------------------------------------+
| "**"                                            | Exponentiation [5]                    |
+-------------------------------------------------+---------------------------------------+
| "+x", "-x", "~x"                                | Positive, negative, bitwise NOT       |
+-------------------------------------------------+---------------------------------------+
| "*", "@", "/", "//", "%"                        | Multiplication, matrix                |
|                                                 | multiplication, division, floor       |
|                                                 | division, remainder [6]               |
+-------------------------------------------------+---------------------------------------+
| "+", "-"                                        | Addition and subtraction              |
+-------------------------------------------------+---------------------------------------+
| "<<", ">>"                                      | Shifts                                |
+-------------------------------------------------+---------------------------------------+
| "&"                                             | Bitwise AND                           |
+-------------------------------------------------+---------------------------------------+
| "^"                                             | Bitwise XOR                           |
+-------------------------------------------------+---------------------------------------+
| "|"                                             | Bitwise OR                            |
+-------------------------------------------------+---------------------------------------+
| "in", "not in", "is", "is not", "<", "<=", ">", | Comparisons, including membership     |
| ">=", "!=", "=="                                | tests and identity tests              |
+-------------------------------------------------+---------------------------------------+
| "not x"                                         | Boolean NOT                           |
+-------------------------------------------------+---------------------------------------+
| "and"                                           | Boolean AND                           |
+-------------------------------------------------+---------------------------------------+
| "or"                                            | Boolean OR                            |
+-------------------------------------------------+---------------------------------------+
| "if" – "else"                                   | Conditional expression                |
+-------------------------------------------------+---------------------------------------+
| "lambda"                                        | Lambda expression                     |
+-------------------------------------------------+---------------------------------------+
| ":="                                            | Assignment expression                 |
+-------------------------------------------------+---------------------------------------+

-[ Footnotes ]-

[1] While "abs(x%y) < abs(y)" is true mathematically, for floats it
    may not be true numerically due to roundoff.  For example, and
    assuming a platform on which a Python float is an IEEE 754 double-
    precision number, in order that "-1e-100 % 1e100" have the same
    sign as "1e100", the computed result is "-1e-100 + 1e100", which
    is numerically exactly equal to "1e100".  The function
    "math.fmod()" returns a result whose sign matches the sign of the
    first argument instead, and so returns "-1e-100" in this case.
    Which approach is more appropriate depends on the application.

[2] If x is very close to an exact integer multiple of y, it’s
    possible for "x//y" to be one larger than "(x-x%y)//y" due to
    rounding.  In such cases, Python returns the latter result, in
    order to preserve that "divmod(x,y)[0] * y + x % y" be very close
    to "x".

[3] The Unicode standard distinguishes between *code points* (e.g.
    U+0041) and *abstract characters* (e.g. “LATIN CAPITAL LETTER A”).
    While most abstract characters in Unicode are only represented
    using one code point, there is a number of abstract characters
    that can in addition be represented using a sequence of more than
    one code point.  For example, the abstract character “LATIN
    CAPITAL LETTER C WITH CEDILLA” can be represented as a single
    *precomposed character* at code position U+00C7, or as a sequence
    of a *base character* at code position U+0043 (LATIN CAPITAL
    LETTER C), followed by a *combining character* at code position
    U+0327 (COMBINING CEDILLA).

    The comparison operators on strings compare at the level of
    Unicode code points. This may be counter-intuitive to humans.  For
    example, ""\u00C7" == "\u0043\u0327"" is "False", even though both
    strings represent the same abstract character “LATIN CAPITAL
    LETTER C WITH CEDILLA”.

    To compare strings at the level of abstract characters (that is,
    in a way intuitive to humans), use "unicodedata.normalize()".

[4] Due to automatic garbage-collection, free lists, and the dynamic
    nature of descriptors, you may notice seemingly unusual behaviour
    in certain uses of the "is" operator, like those involving
    comparisons between instance methods, or constants.  Check their
    documentation for more info.

[5] The power operator "**" binds less tightly than an arithmetic or
    bitwise unary operator on its right, that is, "2**-1" is "0.5".

[6] The "%" operator is also used for string formatting; the same
    precedence applies.
