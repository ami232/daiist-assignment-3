# Python Library Reference: Built-in Types

Source URL: https://docs.python.org/3.13/library/stdtypes.html
Reference version: Python 3.13
Licence: Python Software Foundation License Version 2 (https://docs.python.org/3.13/license.html)
Local extraction: CPython 3.13 pydoc_data.topics generated from the official documentation

### TOPIC: truth
Truth Value Testing
*******************

Any object can be tested for truth value, for use in an "if" or
"while" condition or as operand of the Boolean operations below.

By default, an object is considered true unless its class defines
either a "__bool__()" method that returns "False" or a "__len__()"
method that returns zero, when called with the object. [1]  Here are
most of the built-in objects considered false:

* constants defined to be false: "None" and "False"

* zero of any numeric type: "0", "0.0", "0j", "Decimal(0)",
  "Fraction(0, 1)"

* empty sequences and collections: "''", "()", "[]", "{}", "set()",
  "range(0)"

Operations and built-in functions that have a Boolean result always
return "0" or "False" for false and "1" or "True" for true, unless
otherwise stated. (Important exception: the Boolean operations "or"
and "and" always return one of their operands.)

### TOPIC: typesseq
Sequence Types — "list", "tuple", "range"
*****************************************

There are three basic sequence types: lists, tuples, and range
objects. Additional sequence types tailored for processing of binary
data and text strings are described in dedicated sections.


Common Sequence Operations
==========================

The operations in the following table are supported by most sequence
types, both mutable and immutable. The "collections.abc.Sequence" ABC
is provided to make it easier to correctly implement these operations
on custom sequence types.

This table lists the sequence operations sorted in ascending priority.
In the table, *s* and *t* are sequences of the same type, *n*, *i*,
*j* and *k* are integers and *x* is an arbitrary object that meets any
type and value restrictions imposed by *s*.

The "in" and "not in" operations have the same priorities as the
comparison operations. The "+" (concatenation) and "*" (repetition)
operations have the same priority as the corresponding numeric
operations. [3]

+----------------------------+----------------------------------+------------+
| Operation                  | Result                           | Notes      |
|============================|==================================|============|
| "x in s"                   | "True" if an item of *s* is      | (1)        |
|                            | equal to *x*, else "False"       |            |
+----------------------------+----------------------------------+------------+
| "x not in s"               | "False" if an item of *s* is     | (1)        |
|                            | equal to *x*, else "True"        |            |
+----------------------------+----------------------------------+------------+
| "s + t"                    | the concatenation of *s* and *t* | (6)(7)     |
+----------------------------+----------------------------------+------------+
| "s * n" or "n * s"         | equivalent to adding *s* to      | (2)(7)     |
|                            | itself *n* times                 |            |
+----------------------------+----------------------------------+------------+
| "s[i]"                     | *i*th item of *s*, origin 0      | (3)(9)     |
+----------------------------+----------------------------------+------------+
| "s[i:j]"                   | slice of *s* from *i* to *j*     | (3)(4)     |
+----------------------------+----------------------------------+------------+
| "s[i:j:k]"                 | slice of *s* from *i* to *j*     | (3)(5)     |
|                            | with step *k*                    |            |
+----------------------------+----------------------------------+------------+
| "len(s)"                   | length of *s*                    |            |
+----------------------------+----------------------------------+------------+
| "min(s)"                   | smallest item of *s*             |            |
+----------------------------+----------------------------------+------------+
| "max(s)"                   | largest item of *s*              |            |
+----------------------------+----------------------------------+------------+
| "s.index(x[, i[, j]])"     | index of the first occurrence of | (8)        |
|                            | *x* in *s* (at or after index    |            |
|                            | *i* and before index *j*)        |            |
+----------------------------+----------------------------------+------------+
| "s.count(x)"               | total number of occurrences of   |            |
|                            | *x* in *s*                       |            |
+----------------------------+----------------------------------+------------+

Sequences of the same type also support comparisons.  In particular,
tuples and lists are compared lexicographically by comparing
corresponding elements. This means that to compare equal, every
element must compare equal and the two sequences must be of the same
type and have the same length.  (For full details see Comparisons in
the language reference.)

Forward and reversed iterators over mutable sequences access values
using an index.  That index will continue to march forward (or
backward) even if the underlying sequence is mutated.  The iterator
terminates only when an "IndexError" or a "StopIteration" is
encountered (or when the index drops below zero).

Notes:

1. While the "in" and "not in" operations are used only for simple
   containment testing in the general case, some specialised sequences
   (such as "str", "bytes" and "bytearray") also use them for
   subsequence testing:

      >>> "gg" in "eggs"
      True

2. Values of *n* less than "0" are treated as "0" (which yields an
   empty sequence of the same type as *s*).  Note that items in the
   sequence *s* are not copied; they are referenced multiple times.
   This often haunts new Python programmers; consider:

      >>> lists = [[]] * 3
      >>> lists
      [[], [], []]
      >>> lists[0].append(3)
      >>> lists
      [[3], [3], [3]]

   What has happened is that "[[]]" is a one-element list containing
   an empty list, so all three elements of "[[]] * 3" are references
   to this single empty list.  Modifying any of the elements of
   "lists" modifies this single list. You can create a list of
   different lists this way:

      >>> lists = [[] for i in range(3)]
      >>> lists[0].append(3)
      >>> lists[1].append(5)
      >>> lists[2].append(7)
      >>> lists
      [[3], [5], [7]]

   Further explanation is available in the FAQ entry How do I create a
   multidimensional list?.

3. If *i* or *j* is negative, the index is relative to the end of
   sequence *s*: "len(s) + i" or "len(s) + j" is substituted.  But
   note that "-0" is still "0".

4. The slice of *s* from *i* to *j* is defined as the sequence of
   items with index *k* such that "i <= k < j".  If *i* or *j* is
   greater than "len(s)", use "len(s)".  If *i* is omitted or "None",
   use "0".  If *j* is omitted or "None", use "len(s)".  If *i* is
   greater than or equal to *j*, the slice is empty.

5. The slice of *s* from *i* to *j* with step *k* is defined as the
   sequence of items with index  "x = i + n*k" such that "0 <= n <
   (j-i)/k".  In other words, the indices are "i", "i+k", "i+2*k",
   "i+3*k" and so on, stopping when *j* is reached (but never
   including *j*).  When *k* is positive, *i* and *j* are reduced to
   "len(s)" if they are greater. When *k* is negative, *i* and *j* are
   reduced to "len(s) - 1" if they are greater.  If *i* or *j* are
   omitted or "None", they become “end” values (which end depends on
   the sign of *k*).  Note, *k* cannot be zero. If *k* is "None", it
   is treated like "1".

6. Concatenating immutable sequences always results in a new object.
   This means that building up a sequence by repeated concatenation
   will have a quadratic runtime cost in the total sequence length.
   To get a linear runtime cost, you must switch to one of the
   alternatives below:

   * if concatenating "str" objects, you can build a list and use
     "str.join()" at the end or else write to an "io.StringIO"
     instance and retrieve its value when complete

   * if concatenating "bytes" objects, you can similarly use
     "bytes.join()" or "io.BytesIO", or you can do in-place
     concatenation with a "bytearray" object.  "bytearray" objects are
     mutable and have an efficient overallocation mechanism

   * if concatenating "tuple" objects, extend a "list" instead

   * for other types, investigate the relevant class documentation

7. Some sequence types (such as "range") only support item sequences
   that follow specific patterns, and hence don’t support sequence
   concatenation or repetition.

8. "index" raises "ValueError" when *x* is not found in *s*. Not all
   implementations support passing the additional arguments *i* and
   *j*. These arguments allow efficient searching of subsections of
   the sequence. Passing the extra arguments is roughly equivalent to
   using "s[i:j].index(x)", only without copying any data and with the
   returned index being relative to the start of the sequence rather
   than the start of the slice.

9. An "IndexError" is raised if *i* is outside the sequence range.


Immutable Sequence Types
========================

The only operation that immutable sequence types generally implement
that is not also implemented by mutable sequence types is support for
the "hash()" built-in.

This support allows immutable sequences, such as "tuple" instances, to
be used as "dict" keys and stored in "set" and "frozenset" instances.

Attempting to hash an immutable sequence that contains unhashable
values will result in "TypeError".


Mutable Sequence Types
======================

The operations in the following table are defined on mutable sequence
types. The "collections.abc.MutableSequence" ABC is provided to make
it easier to correctly implement these operations on custom sequence
types.

In the table *s* is an instance of a mutable sequence type, *t* is any
iterable object and *x* is an arbitrary object that meets any type and
value restrictions imposed by *s* (for example, "bytearray" only
accepts integers that meet the value restriction "0 <= x <= 255").

+--------------------------------+----------------------------------+-----------------------+
| Operation                      | Result                           | Notes                 |
|================================|==================================|=======================|
| "s[i] = x"                     | item *i* of *s* is replaced by   |                       |
|                                | *x*                              |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i]"                     | removes item *i* of *s*          |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s[i:j] = t"                   | slice of *s* from *i* to *j* is  |                       |
|                                | replaced by the contents of the  |                       |
|                                | iterable *t*                     |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i:j]"                   | same as "s[i:j] = []"            |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s[i:j:k] = t"                 | the elements of "s[i:j:k]" are   | (1)                   |
|                                | replaced by those of *t*         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i:j:k]"                 | removes the elements of          |                       |
|                                | "s[i:j:k]" from the list         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.append(x)"                  | appends *x* to the end of the    |                       |
|                                | sequence (same as                |                       |
|                                | "s[len(s):len(s)] = [x]")        |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.clear()"                    | removes all items from *s* (same | (5)                   |
|                                | as "del s[:]")                   |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.copy()"                     | creates a shallow copy of *s*    | (5)                   |
|                                | (same as "s[:]")                 |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.extend(t)" or "s += t"      | extends *s* with the contents of |                       |
|                                | *t* (for the most part the same  |                       |
|                                | as "s[len(s):len(s)] = t")       |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s *= n"                       | updates *s* with its contents    | (6)                   |
|                                | repeated *n* times               |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.insert(i, x)"               | inserts *x* into *s* at the      |                       |
|                                | index given by *i* (same as      |                       |
|                                | "s[i:i] = [x]")                  |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.pop()" or "s.pop(i)"        | retrieves the item at *i* and    | (2)                   |
|                                | also removes it from *s*         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.remove(x)"                  | removes the first item from *s*  | (3)                   |
|                                | where "s[i]" is equal to *x*     |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.reverse()"                  | reverses the items of *s* in     | (4)                   |
|                                | place                            |                       |
+--------------------------------+----------------------------------+-----------------------+

Notes:

1. If *k* is not equal to "1", *t* must have the same length as the
   slice it is replacing.

2. The optional argument *i* defaults to "-1", so that by default the
   last item is removed and returned.

3. "remove()" raises "ValueError" when *x* is not found in *s*.

4. The "reverse()" method modifies the sequence in place for economy
   of space when reversing a large sequence.  To remind users that it
   operates by side effect, it does not return the reversed sequence.

5. "clear()" and "copy()" are included for consistency with the
   interfaces of mutable containers that don’t support slicing
   operations (such as "dict" and "set"). "copy()" is not part of the
   "collections.abc.MutableSequence" ABC, but most concrete mutable
   sequence classes provide it.

   Added in version 3.3: "clear()" and "copy()" methods.

6. The value *n* is an integer, or an object implementing
   "__index__()".  Zero and negative values of *n* clear the sequence.
   Items in the sequence are not copied; they are referenced multiple
   times, as explained for "s * n" under Common Sequence Operations.


Lists
=====

Lists are mutable sequences, typically used to store collections of
homogeneous items (where the precise degree of similarity will vary by
application).

class list([iterable])

   Lists may be constructed in several ways:

   * Using a pair of square brackets to denote the empty list: "[]"

   * Using square brackets, separating items with commas: "[a]", "[a,
     b, c]"

   * Using a list comprehension: "[x for x in iterable]"

   * Using the type constructor: "list()" or "list(iterable)"

   The constructor builds a list whose items are the same and in the
   same order as *iterable*’s items.  *iterable* may be either a
   sequence, a container that supports iteration, or an iterator
   object.  If *iterable* is already a list, a copy is made and
   returned, similar to "iterable[:]". For example, "list('abc')"
   returns "['a', 'b', 'c']" and "list( (1, 2, 3) )" returns "[1, 2,
   3]". If no argument is given, the constructor creates a new empty
   list, "[]".

   Many other operations also produce lists, including the "sorted()"
   built-in.

   Lists implement all of the common and mutable sequence operations.
   Lists also provide the following additional method:

   sort(*, key=None, reverse=False)

      This method sorts the list in place, using only "<" comparisons
      between items. Exceptions are not suppressed - if any comparison
      operations fail, the entire sort operation will fail (and the
      list will likely be left in a partially modified state).

      "sort()" accepts two arguments that can only be passed by
      keyword (keyword-only arguments):

      *key* specifies a function of one argument that is used to
      extract a comparison key from each list element (for example,
      "key=str.lower"). The key corresponding to each item in the list
      is calculated once and then used for the entire sorting process.
      The default value of "None" means that list items are sorted
      directly without calculating a separate key value.

      The "functools.cmp_to_key()" utility is available to convert a
      2.x style *cmp* function to a *key* function.

      *reverse* is a boolean value.  If set to "True", then the list
      elements are sorted as if each comparison were reversed.

      This method modifies the sequence in place for economy of space
      when sorting a large sequence.  To remind users that it operates
      by side effect, it does not return the sorted sequence (use
      "sorted()" to explicitly request a new sorted list instance).

      The "sort()" method is guaranteed to be stable.  A sort is
      stable if it guarantees not to change the relative order of
      elements that compare equal — this is helpful for sorting in
      multiple passes (for example, sort by department, then by salary
      grade).

      For sorting examples and a brief sorting tutorial, see Sorting
      Techniques.

      **CPython implementation detail:** While a list is being sorted,
      the effect of attempting to mutate, or even inspect, the list is
      undefined.  The C implementation of Python makes the list appear
      empty for the duration, and raises "ValueError" if it can detect
      that the list has been mutated during a sort.


Tuples
======

Tuples are immutable sequences, typically used to store collections of
heterogeneous data (such as the 2-tuples produced by the "enumerate()"
built-in). Tuples are also used for cases where an immutable sequence
of homogeneous data is needed (such as allowing storage in a "set" or
"dict" instance).

class tuple([iterable])

   Tuples may be constructed in a number of ways:

   * Using a pair of parentheses to denote the empty tuple: "()"

   * Using a trailing comma for a singleton tuple: "a," or "(a,)"

   * Separating items with commas: "a, b, c" or "(a, b, c)"

   * Using the "tuple()" built-in: "tuple()" or "tuple(iterable)"

   The constructor builds a tuple whose items are the same and in the
   same order as *iterable*’s items.  *iterable* may be either a
   sequence, a container that supports iteration, or an iterator
   object.  If *iterable* is already a tuple, it is returned
   unchanged. For example, "tuple('abc')" returns "('a', 'b', 'c')"
   and "tuple( [1, 2, 3] )" returns "(1, 2, 3)". If no argument is
   given, the constructor creates a new empty tuple, "()".

   Note that it is actually the comma which makes a tuple, not the
   parentheses. The parentheses are optional, except in the empty
   tuple case, or when they are needed to avoid syntactic ambiguity.
   For example, "f(a, b, c)" is a function call with three arguments,
   while "f((a, b, c))" is a function call with a 3-tuple as the sole
   argument.

   Tuples implement all of the common sequence operations.

For heterogeneous collections of data where access by name is clearer
than access by index, "collections.namedtuple()" may be a more
appropriate choice than a simple tuple object.


Ranges
======

The "range" type represents an immutable sequence of numbers and is
commonly used for looping a specific number of times in "for" loops.

class range(stop)
class range(start, stop[, step])

   The arguments to the range constructor must be integers (either
   built-in "int" or any object that implements the "__index__()"
   special method).  If the *step* argument is omitted, it defaults to
   "1". If the *start* argument is omitted, it defaults to "0". If
   *step* is zero, "ValueError" is raised.

   For a positive *step*, the contents of a range "r" are determined
   by the formula "r[i] = start + step*i" where "i >= 0" and "r[i] <
   stop".

   For a negative *step*, the contents of the range are still
   determined by the formula "r[i] = start + step*i", but the
   constraints are "i >= 0" and "r[i] > stop".

   A range object will be empty if "r[0]" does not meet the value
   constraint. Ranges do support negative indices, but these are
   interpreted as indexing from the end of the sequence determined by
   the positive indices.

   Ranges containing absolute values larger than "sys.maxsize" are
   permitted but some features (such as "len()") may raise
   "OverflowError".

   Range examples:

      >>> list(range(10))
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      >>> list(range(1, 11))
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      >>> list(range(0, 30, 5))
      [0, 5, 10, 15, 20, 25]
      >>> list(range(0, 10, 3))
      [0, 3, 6, 9]
      >>> list(range(0, -10, -1))
      [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
      >>> list(range(0))
      []
      >>> list(range(1, 0))
      []

   Ranges implement all of the common sequence operations except
   concatenation and repetition (due to the fact that range objects
   can only represent sequences that follow a strict pattern and
   repetition and concatenation will usually violate that pattern).

   start

      The value of the *start* parameter (or "0" if the parameter was
      not supplied)

   stop

      The value of the *stop* parameter

   step

      The value of the *step* parameter (or "1" if the parameter was
      not supplied)

The advantage of the "range" type over a regular "list" or "tuple" is
that a "range" object will always take the same (small) amount of
memory, no matter the size of the range it represents (as it only
stores the "start", "stop" and "step" values, calculating individual
items and subranges as needed).

Range objects implement the "collections.abc.Sequence" ABC, and
provide features such as containment tests, element index lookup,
slicing and support for negative indices (see Sequence Types — list,
tuple, range):

>>> r = range(0, 20, 2)
>>> r
range(0, 20, 2)
>>> 11 in r
False
>>> 10 in r
True
>>> r.index(10)
5
>>> r[5]
10
>>> r[:5]
range(0, 10, 2)
>>> r[-1]
18

Testing range objects for equality with "==" and "!=" compares them as
sequences.  That is, two range objects are considered equal if they
represent the same sequence of values.  (Note that two range objects
that compare equal might have different "start", "stop" and "step"
attributes, for example "range(0) == range(2, 1, 3)" or "range(0, 3,
2) == range(0, 4, 2)".)

Changed in version 3.2: Implement the Sequence ABC. Support slicing
and negative indices. Test "int" objects for membership in constant
time instead of iterating through all items.

Changed in version 3.3: Define ‘==’ and ‘!=’ to compare range objects
based on the sequence of values they define (instead of comparing
based on object identity).Added the "start", "stop" and "step"
attributes.

See also:

  * The linspace recipe shows how to implement a lazy version of range
    suitable for floating-point applications.

### TOPIC: typesseq-mutable
Mutable Sequence Types
**********************

The operations in the following table are defined on mutable sequence
types. The "collections.abc.MutableSequence" ABC is provided to make
it easier to correctly implement these operations on custom sequence
types.

In the table *s* is an instance of a mutable sequence type, *t* is any
iterable object and *x* is an arbitrary object that meets any type and
value restrictions imposed by *s* (for example, "bytearray" only
accepts integers that meet the value restriction "0 <= x <= 255").

+--------------------------------+----------------------------------+-----------------------+
| Operation                      | Result                           | Notes                 |
|================================|==================================|=======================|
| "s[i] = x"                     | item *i* of *s* is replaced by   |                       |
|                                | *x*                              |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i]"                     | removes item *i* of *s*          |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s[i:j] = t"                   | slice of *s* from *i* to *j* is  |                       |
|                                | replaced by the contents of the  |                       |
|                                | iterable *t*                     |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i:j]"                   | same as "s[i:j] = []"            |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s[i:j:k] = t"                 | the elements of "s[i:j:k]" are   | (1)                   |
|                                | replaced by those of *t*         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "del s[i:j:k]"                 | removes the elements of          |                       |
|                                | "s[i:j:k]" from the list         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.append(x)"                  | appends *x* to the end of the    |                       |
|                                | sequence (same as                |                       |
|                                | "s[len(s):len(s)] = [x]")        |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.clear()"                    | removes all items from *s* (same | (5)                   |
|                                | as "del s[:]")                   |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.copy()"                     | creates a shallow copy of *s*    | (5)                   |
|                                | (same as "s[:]")                 |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.extend(t)" or "s += t"      | extends *s* with the contents of |                       |
|                                | *t* (for the most part the same  |                       |
|                                | as "s[len(s):len(s)] = t")       |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s *= n"                       | updates *s* with its contents    | (6)                   |
|                                | repeated *n* times               |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.insert(i, x)"               | inserts *x* into *s* at the      |                       |
|                                | index given by *i* (same as      |                       |
|                                | "s[i:i] = [x]")                  |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.pop()" or "s.pop(i)"        | retrieves the item at *i* and    | (2)                   |
|                                | also removes it from *s*         |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.remove(x)"                  | removes the first item from *s*  | (3)                   |
|                                | where "s[i]" is equal to *x*     |                       |
+--------------------------------+----------------------------------+-----------------------+
| "s.reverse()"                  | reverses the items of *s* in     | (4)                   |
|                                | place                            |                       |
+--------------------------------+----------------------------------+-----------------------+

Notes:

1. If *k* is not equal to "1", *t* must have the same length as the
   slice it is replacing.

2. The optional argument *i* defaults to "-1", so that by default the
   last item is removed and returned.

3. "remove()" raises "ValueError" when *x* is not found in *s*.

4. The "reverse()" method modifies the sequence in place for economy
   of space when reversing a large sequence.  To remind users that it
   operates by side effect, it does not return the reversed sequence.

5. "clear()" and "copy()" are included for consistency with the
   interfaces of mutable containers that don’t support slicing
   operations (such as "dict" and "set"). "copy()" is not part of the
   "collections.abc.MutableSequence" ABC, but most concrete mutable
   sequence classes provide it.

   Added in version 3.3: "clear()" and "copy()" methods.

6. The value *n* is an integer, or an object implementing
   "__index__()".  Zero and negative values of *n* clear the sequence.
   Items in the sequence are not copied; they are referenced multiple
   times, as explained for "s * n" under Common Sequence Operations.

### TOPIC: typesmapping
Mapping Types — "dict"
**********************

A *mapping* object maps *hashable* values to arbitrary objects.
Mappings are mutable objects.  There is currently only one standard
mapping type, the *dictionary*.  (For other containers see the built-
in "list", "set", and "tuple" classes, and the "collections" module.)

A dictionary’s keys are *almost* arbitrary values.  Values that are
not *hashable*, that is, values containing lists, dictionaries or
other mutable types (that are compared by value rather than by object
identity) may not be used as keys. Values that compare equal (such as
"1", "1.0", and "True") can be used interchangeably to index the same
dictionary entry.

class dict(**kwargs)
class dict(mapping, **kwargs)
class dict(iterable, **kwargs)

   Return a new dictionary initialized from an optional positional
   argument and a possibly empty set of keyword arguments.

   Dictionaries can be created by several means:

   * Use a comma-separated list of "key: value" pairs within braces:
     "{'jack': 4098, 'sjoerd': 4127}" or "{4098: 'jack', 4127:
     'sjoerd'}"

   * Use a dict comprehension: "{}", "{x: x ** 2 for x in range(10)}"

   * Use the type constructor: "dict()", "dict([('foo', 100), ('bar',
     200)])", "dict(foo=100, bar=200)"

   If no positional argument is given, an empty dictionary is created.
   If a positional argument is given and it defines a "keys()" method,
   a dictionary is created by calling "__getitem__()" on the argument
   with each returned key from the method.  Otherwise, the positional
   argument must be an *iterable* object.  Each item in the iterable
   must itself be an iterable with exactly two elements.  The first
   element of each item becomes a key in the new dictionary, and the
   second element the corresponding value.  If a key occurs more than
   once, the last value for that key becomes the corresponding value
   in the new dictionary.

   If keyword arguments are given, the keyword arguments and their
   values are added to the dictionary created from the positional
   argument.  If a key being added is already present, the value from
   the keyword argument replaces the value from the positional
   argument.

   Providing keyword arguments as in the first example only works for
   keys that are valid Python identifiers.  Otherwise, any valid keys
   can be used.

   Dictionaries compare equal if and only if they have the same "(key,
   value)" pairs (regardless of ordering). Order comparisons (‘<’,
   ‘<=’, ‘>=’, ‘>’) raise "TypeError".  To illustrate dictionary
   creation and equality, the following examples all return a
   dictionary equal to "{"one": 1, "two": 2, "three": 3}":

      >>> a = dict(one=1, two=2, three=3)
      >>> b = {'one': 1, 'two': 2, 'three': 3}
      >>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
      >>> d = dict([('two', 2), ('one', 1), ('three', 3)])
      >>> e = dict({'three': 3, 'one': 1, 'two': 2})
      >>> f = dict({'one': 1, 'three': 3}, two=2)
      >>> a == b == c == d == e == f
      True

   Providing keyword arguments as in the first example only works for
   keys that are valid Python identifiers.  Otherwise, any valid keys
   can be used.

   Dictionaries preserve insertion order.  Note that updating a key
   does not affect the order.  Keys added after deletion are inserted
   at the end.

      >>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
      >>> d
      {'one': 1, 'two': 2, 'three': 3, 'four': 4}
      >>> list(d)
      ['one', 'two', 'three', 'four']
      >>> list(d.values())
      [1, 2, 3, 4]
      >>> d["one"] = 42
      >>> d
      {'one': 42, 'two': 2, 'three': 3, 'four': 4}
      >>> del d["two"]
      >>> d["two"] = None
      >>> d
      {'one': 42, 'three': 3, 'four': 4, 'two': None}

   Changed in version 3.7: Dictionary order is guaranteed to be
   insertion order.  This behavior was an implementation detail of
   CPython from 3.6.

   These are the operations that dictionaries support (and therefore,
   custom mapping types should support too):

   list(d)

      Return a list of all the keys used in the dictionary *d*.

   len(d)

      Return the number of items in the dictionary *d*.

   d[key]

      Return the item of *d* with key *key*.  Raises a "KeyError" if
      *key* is not in the map.

      If a subclass of dict defines a method "__missing__()" and *key*
      is not present, the "d[key]" operation calls that method with
      the key *key* as argument.  The "d[key]" operation then returns
      or raises whatever is returned or raised by the
      "__missing__(key)" call. No other operations or methods invoke
      "__missing__()". If "__missing__()" is not defined, "KeyError"
      is raised. "__missing__()" must be a method; it cannot be an
      instance variable:

         >>> class Counter(dict):
         ...     def __missing__(self, key):
         ...         return 0
         ...
         >>> c = Counter()
         >>> c['red']
         0
         >>> c['red'] += 1
         >>> c['red']
         1

      The example above shows part of the implementation of
      "collections.Counter".  A different "__missing__" method is used
      by "collections.defaultdict".

   d[key] = value

      Set "d[key]" to *value*.

   del d[key]

      Remove "d[key]" from *d*.  Raises a "KeyError" if *key* is not
      in the map.

   key in d

      Return "True" if *d* has a key *key*, else "False".

   key not in d

      Equivalent to "not key in d".

   iter(d)

      Return an iterator over the keys of the dictionary.  This is a
      shortcut for "iter(d.keys())".

   clear()

      Remove all items from the dictionary.

   copy()

      Return a shallow copy of the dictionary.

   classmethod fromkeys(iterable, value=None, /)

      Create a new dictionary with keys from *iterable* and values set
      to *value*.

      "fromkeys()" is a class method that returns a new dictionary.
      *value* defaults to "None".  All of the values refer to just a
      single instance, so it generally doesn’t make sense for *value*
      to be a mutable object such as an empty list.  To get distinct
      values, use a dict comprehension instead.

   get(key, default=None, /)

      Return the value for *key* if *key* is in the dictionary, else
      *default*. If *default* is not given, it defaults to "None", so
      that this method never raises a "KeyError".

   items()

      Return a new view of the dictionary’s items ("(key, value)"
      pairs). See the documentation of view objects.

   keys()

      Return a new view of the dictionary’s keys.  See the
      documentation of view objects.

   pop(key[, default])

      If *key* is in the dictionary, remove it and return its value,
      else return *default*.  If *default* is not given and *key* is
      not in the dictionary, a "KeyError" is raised.

   popitem()

      Remove and return a "(key, value)" pair from the dictionary.
      Pairs are returned in LIFO (last-in, first-out) order.

      "popitem()" is useful to destructively iterate over a
      dictionary, as often used in set algorithms.  If the dictionary
      is empty, calling "popitem()" raises a "KeyError".

      Changed in version 3.7: LIFO order is now guaranteed. In prior
      versions, "popitem()" would return an arbitrary key/value pair.

   reversed(d)

      Return a reverse iterator over the keys of the dictionary. This
      is a shortcut for "reversed(d.keys())".

      Added in version 3.8.

   setdefault(key, default=None, /)

      If *key* is in the dictionary, return its value.  If not, insert
      *key* with a value of *default* and return *default*.  *default*
      defaults to "None".

   update([other])

      Update the dictionary with the key/value pairs from *other*,
      overwriting existing keys.  Return "None".

      "update()" accepts either another object with a "keys()" method
      (in which case "__getitem__()" is called with every key returned
      from the method) or an iterable of key/value pairs (as tuples or
      other iterables of length two). If keyword arguments are
      specified, the dictionary is then updated with those key/value
      pairs: "d.update(red=1, blue=2)".

   values()

      Return a new view of the dictionary’s values.  See the
      documentation of view objects.

      An equality comparison between one "dict.values()" view and
      another will always return "False". This also applies when
      comparing "dict.values()" to itself:

         >>> d = {'a': 1}
         >>> d.values() == d.values()
         False

   d | other

      Create a new dictionary with the merged keys and values of *d*
      and *other*, which must both be dictionaries. The values of
      *other* take priority when *d* and *other* share keys.

      Added in version 3.9.

   d |= other

      Update the dictionary *d* with keys and values from *other*,
      which may be either a *mapping* or an *iterable* of key/value
      pairs. The values of *other* take priority when *d* and *other*
      share keys.

      Added in version 3.9.

   Dictionaries and dictionary views are reversible.

      >>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
      >>> d
      {'one': 1, 'two': 2, 'three': 3, 'four': 4}
      >>> list(reversed(d))
      ['four', 'three', 'two', 'one']
      >>> list(reversed(d.values()))
      [4, 3, 2, 1]
      >>> list(reversed(d.items()))
      [('four', 4), ('three', 3), ('two', 2), ('one', 1)]

   Changed in version 3.8: Dictionaries are now reversible.

See also:

  "types.MappingProxyType" can be used to create a read-only view of a
  "dict".


Dictionary view objects
=======================

The objects returned by "dict.keys()", "dict.values()" and
"dict.items()" are *view objects*.  They provide a dynamic view on the
dictionary’s entries, which means that when the dictionary changes,
the view reflects these changes.

Dictionary views can be iterated over to yield their respective data,
and support membership tests:

len(dictview)

   Return the number of entries in the dictionary.

iter(dictview)

   Return an iterator over the keys, values or items (represented as
   tuples of "(key, value)") in the dictionary.

   Keys and values are iterated over in insertion order. This allows
   the creation of "(value, key)" pairs using "zip()": "pairs =
   zip(d.values(), d.keys())".  Another way to create the same list is
   "pairs = [(v, k) for (k, v) in d.items()]".

   Iterating views while adding or deleting entries in the dictionary
   may raise a "RuntimeError" or fail to iterate over all entries.

   Changed in version 3.7: Dictionary order is guaranteed to be
   insertion order.

x in dictview

   Return "True" if *x* is in the underlying dictionary’s keys, values
   or items (in the latter case, *x* should be a "(key, value)"
   tuple).

reversed(dictview)

   Return a reverse iterator over the keys, values or items of the
   dictionary. The view will be iterated in reverse order of the
   insertion.

   Changed in version 3.8: Dictionary views are now reversible.

dictview.mapping

   Return a "types.MappingProxyType" that wraps the original
   dictionary to which the view refers.

   Added in version 3.10.

Keys views are set-like since their entries are unique and *hashable*.
Items views also have set-like operations since the (key, value) pairs
are unique and the keys are hashable. If all values in an items view
are hashable as well, then the items view can interoperate with other
sets. (Values views are not treated as set-like since the entries are
generally not unique.)  For set-like views, all of the operations
defined for the abstract base class "collections.abc.Set" are
available (for example, "==", "<", or "^").  While using set
operators, set-like views accept any iterable as the other operand,
unlike sets which only accept sets as the input.

An example of dictionary view usage:

   >>> dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}
   >>> keys = dishes.keys()
   >>> values = dishes.values()

   >>> # iteration
   >>> n = 0
   >>> for val in values:
   ...     n += val
   ...
   >>> print(n)
   504

   >>> # keys and values are iterated over in the same order (insertion order)
   >>> list(keys)
   ['eggs', 'sausage', 'bacon', 'spam']
   >>> list(values)
   [2, 1, 1, 500]

   >>> # view objects are dynamic and reflect dict changes
   >>> del dishes['eggs']
   >>> del dishes['sausage']
   >>> list(keys)
   ['bacon', 'spam']

   >>> # set operations
   >>> keys & {'eggs', 'bacon', 'salad'}
   {'bacon'}
   >>> keys ^ {'sausage', 'juice'} == {'juice', 'sausage', 'bacon', 'spam'}
   True
   >>> keys | ['juice', 'juice', 'juice'] == {'bacon', 'spam', 'juice'}
   True

   >>> # get back a read-only proxy for the original dictionary
   >>> values.mapping
   mappingproxy({'bacon': 1, 'spam': 500})
   >>> values.mapping['spam']
   500

### TOPIC: string-methods
String Methods
**************

Strings implement all of the common sequence operations, along with
the additional methods described below.

Strings also support two styles of string formatting, one providing a
large degree of flexibility and customization (see "str.format()",
Format String Syntax and Custom String Formatting) and the other based
on C "printf" style formatting that handles a narrower range of types
and is slightly harder to use correctly, but is often faster for the
cases it can handle (printf-style String Formatting).

The Text Processing Services section of the standard library covers a
number of other modules that provide various text related utilities
(including regular expression support in the "re" module).

str.capitalize()

   Return a copy of the string with its first character capitalized
   and the rest lowercased.

   Changed in version 3.8: The first character is now put into
   titlecase rather than uppercase. This means that characters like
   digraphs will only have their first letter capitalized, instead of
   the full character.

str.casefold()

   Return a casefolded copy of the string. Casefolded strings may be
   used for caseless matching.

   Casefolding is similar to lowercasing but more aggressive because
   it is intended to remove all case distinctions in a string. For
   example, the German lowercase letter "'ß'" is equivalent to ""ss"".
   Since it is already lowercase, "lower()" would do nothing to "'ß'";
   "casefold()" converts it to ""ss"".

   The casefolding algorithm is described in section 3.13 ‘Default
   Case Folding’ of the Unicode Standard.

   Added in version 3.3.

str.center(width[, fillchar])

   Return centered in a string of length *width*. Padding is done
   using the specified *fillchar* (default is an ASCII space). The
   original string is returned if *width* is less than or equal to
   "len(s)".  For example:

      >>> 'Python'.center(10)
      '  Python  '
      >>> 'Python'.center(10, '-')
      '--Python--'
      >>> 'Python'.center(4)
      'Python'

str.count(sub[, start[, end]])

   Return the number of non-overlapping occurrences of substring *sub*
   in the range [*start*, *end*].  Optional arguments *start* and
   *end* are interpreted as in slice notation.

   If *sub* is empty, returns the number of empty strings between
   characters which is the length of the string plus one. For example:

      >>> 'spam, spam, spam'.count('spam')
      3
      >>> 'spam, spam, spam'.count('spam', 5)
      2
      >>> 'spam, spam, spam'.count('spam', 5, 10)
      1
      >>> 'spam, spam, spam'.count('eggs')
      0
      >>> 'spam, spam, spam'.count('')
      17

str.encode(encoding='utf-8', errors='strict')

   Return the string encoded to "bytes".

   *encoding* defaults to "'utf-8'"; see Standard Encodings for
   possible values.

   *errors* controls how encoding errors are handled. If "'strict'"
   (the default), a "UnicodeError" exception is raised. Other possible
   values are "'ignore'", "'replace'", "'xmlcharrefreplace'",
   "'backslashreplace'" and any other name registered via
   "codecs.register_error()". See Error Handlers for details.

   For performance reasons, the value of *errors* is not checked for
   validity unless an encoding error actually occurs, Python
   Development Mode is enabled or a debug build is used.

   Changed in version 3.1: Added support for keyword arguments.

   Changed in version 3.9: The value of the *errors* argument is now
   checked in Python Development Mode and in debug mode.

str.endswith(suffix[, start[, end]])

   Return "True" if the string ends with the specified *suffix*,
   otherwise return "False".  *suffix* can also be a tuple of suffixes
   to look for.  With optional *start*, test beginning at that
   position.  With optional *end*, stop comparing at that position.

str.expandtabs(tabsize=8)

   Return a copy of the string where all tab characters are replaced
   by one or more spaces, depending on the current column and the
   given tab size.  Tab positions occur every *tabsize* characters
   (default is 8, giving tab positions at columns 0, 8, 16 and so on).
   To expand the string, the current column is set to zero and the
   string is examined character by character.  If the character is a
   tab ("\t"), one or more space characters are inserted in the result
   until the current column is equal to the next tab position. (The
   tab character itself is not copied.)  If the character is a newline
   ("\n") or return ("\r"), it is copied and the current column is
   reset to zero.  Any other character is copied unchanged and the
   current column is incremented by one regardless of how the
   character is represented when printed.

   >>> '01\t012\t0123\t01234'.expandtabs()
   '01      012     0123    01234'
   >>> '01\t012\t0123\t01234'.expandtabs(4)
   '01  012 0123    01234'

str.find(sub[, start[, end]])

   Return the lowest index in the string where substring *sub* is
   found within the slice "s[start:end]".  Optional arguments *start*
   and *end* are interpreted as in slice notation.  Return "-1" if
   *sub* is not found.

   Note:

     The "find()" method should be used only if you need to know the
     position of *sub*.  To check if *sub* is a substring or not, use
     the "in" operator:

        >>> 'Py' in 'Python'
        True

str.format(*args, **kwargs)

   Perform a string formatting operation.  The string on which this
   method is called can contain literal text or replacement fields
   delimited by braces "{}".  Each replacement field contains either
   the numeric index of a positional argument, or the name of a
   keyword argument.  Returns a copy of the string where each
   replacement field is replaced with the string value of the
   corresponding argument.

   >>> "The sum of 1 + 2 is {0}".format(1+2)
   'The sum of 1 + 2 is 3'

   See Format String Syntax for a description of the various
   formatting options that can be specified in format strings.

   Note:

     When formatting a number ("int", "float", "complex",
     "decimal.Decimal" and subclasses) with the "n" type (ex:
     "'{:n}'.format(1234)"), the function temporarily sets the
     "LC_CTYPE" locale to the "LC_NUMERIC" locale to decode
     "decimal_point" and "thousands_sep" fields of "localeconv()" if
     they are non-ASCII or longer than 1 byte, and the "LC_NUMERIC"
     locale is different than the "LC_CTYPE" locale.  This temporary
     change affects other threads.

   Changed in version 3.7: When formatting a number with the "n" type,
   the function sets temporarily the "LC_CTYPE" locale to the
   "LC_NUMERIC" locale in some cases.

str.format_map(mapping, /)

   Similar to "str.format(**mapping)", except that "mapping" is used
   directly and not copied to a "dict".  This is useful if for example
   "mapping" is a dict subclass:

   >>> class Default(dict):
   ...     def __missing__(self, key):
   ...         return key
   ...
   >>> '{name} was born in {country}'.format_map(Default(name='Guido'))
   'Guido was born in country'

   Added in version 3.2.

str.index(sub[, start[, end]])

   Like "find()", but raise "ValueError" when the substring is not
   found.

str.isalnum()

   Return "True" if all characters in the string are alphanumeric and
   there is at least one character, "False" otherwise.  A character
   "c" is alphanumeric if one of the following returns "True":
   "c.isalpha()", "c.isdecimal()", "c.isdigit()", or "c.isnumeric()".

str.isalpha()

   Return "True" if all characters in the string are alphabetic and
   there is at least one character, "False" otherwise.  Alphabetic
   characters are those characters defined in the Unicode character
   database as “Letter”, i.e., those with general category property
   being one of “Lm”, “Lt”, “Lu”, “Ll”, or “Lo”.  Note that this is
   different from the Alphabetic property defined in the section 4.10
   ‘Letters, Alphabetic, and Ideographic’ of the Unicode Standard.

str.isascii()

   Return "True" if the string is empty or all characters in the
   string are ASCII, "False" otherwise. ASCII characters have code
   points in the range U+0000-U+007F.

   Added in version 3.7.

str.isdecimal()

   Return "True" if all characters in the string are decimal
   characters and there is at least one character, "False" otherwise.
   Decimal characters are those that can be used to form numbers in
   base 10, e.g. U+0660, ARABIC-INDIC DIGIT ZERO.  Formally a decimal
   character is a character in the Unicode General Category “Nd”.

str.isdigit()

   Return "True" if all characters in the string are digits and there
   is at least one character, "False" otherwise.  Digits include
   decimal characters and digits that need special handling, such as
   the compatibility superscript digits. This covers digits which
   cannot be used to form numbers in base 10, like the Kharosthi
   numbers.  Formally, a digit is a character that has the property
   value Numeric_Type=Digit or Numeric_Type=Decimal.

str.isidentifier()

   Return "True" if the string is a valid identifier according to the
   language definition, section Identifiers and keywords.

   "keyword.iskeyword()" can be used to test whether string "s" is a
   reserved identifier, such as "def" and "class".

   Example:

      >>> from keyword import iskeyword

      >>> 'hello'.isidentifier(), iskeyword('hello')
      (True, False)
      >>> 'def'.isidentifier(), iskeyword('def')
      (True, True)

str.islower()

   Return "True" if all cased characters [4] in the string are
   lowercase and there is at least one cased character, "False"
   otherwise.

str.isnumeric()

   Return "True" if all characters in the string are numeric
   characters, and there is at least one character, "False" otherwise.
   Numeric characters include digit characters, and all characters
   that have the Unicode numeric value property, e.g. U+2155, VULGAR
   FRACTION ONE FIFTH.  Formally, numeric characters are those with
   the property value Numeric_Type=Digit, Numeric_Type=Decimal or
   Numeric_Type=Numeric.

str.isprintable()

   Return "True" if all characters in the string are printable,
   "False" if it contains at least one non-printable character.

   Here “printable” means the character is suitable for "repr()" to
   use in its output; “non-printable” means that "repr()" on built-in
   types will hex-escape the character.  It has no bearing on the
   handling of strings written to "sys.stdout" or "sys.stderr".

   The printable characters are those which in the Unicode character
   database (see "unicodedata") have a general category in group
   Letter, Mark, Number, Punctuation, or Symbol (L, M, N, P, or S);
   plus the ASCII space 0x20. Nonprintable characters are those in
   group Separator or Other (Z or C), except the ASCII space.

str.isspace()

   Return "True" if there are only whitespace characters in the string
   and there is at least one character, "False" otherwise.

   A character is *whitespace* if in the Unicode character database
   (see "unicodedata"), either its general category is "Zs"
   (“Separator, space”), or its bidirectional class is one of "WS",
   "B", or "S".

str.istitle()

   Return "True" if the string is a titlecased string and there is at
   least one character, for example uppercase characters may only
   follow uncased characters and lowercase characters only cased ones.
   Return "False" otherwise.

str.isupper()

   Return "True" if all cased characters [4] in the string are
   uppercase and there is at least one cased character, "False"
   otherwise.

   >>> 'BANANA'.isupper()
   True
   >>> 'banana'.isupper()
   False
   >>> 'baNana'.isupper()
   False
   >>> ' '.isupper()
   False

str.join(iterable)

   Return a string which is the concatenation of the strings in
   *iterable*. A "TypeError" will be raised if there are any non-
   string values in *iterable*, including "bytes" objects.  The
   separator between elements is the string providing this method.

str.ljust(width[, fillchar])

   Return the string left justified in a string of length *width*.
   Padding is done using the specified *fillchar* (default is an ASCII
   space). The original string is returned if *width* is less than or
   equal to "len(s)".

str.lower()

   Return a copy of the string with all the cased characters [4]
   converted to lowercase.

   The lowercasing algorithm used is described in section 3.13
   ‘Default Case Folding’ of the Unicode Standard.

str.lstrip([chars])

   Return a copy of the string with leading characters removed.  The
   *chars* argument is a string specifying the set of characters to be
   removed.  If omitted or "None", the *chars* argument defaults to
   removing whitespace.  The *chars* argument is not a prefix; rather,
   all combinations of its values are stripped:

      >>> '   spacious   '.lstrip()
      'spacious   '
      >>> 'www.example.com'.lstrip('cmowz.')
      'example.com'

   See "str.removeprefix()" for a method that will remove a single
   prefix string rather than all of a set of characters.  For example:

      >>> 'Arthur: three!'.lstrip('Arthur: ')
      'ee!'
      >>> 'Arthur: three!'.removeprefix('Arthur: ')
      'three!'

static str.maketrans(x[, y[, z]])

   This static method returns a translation table usable for
   "str.translate()".

   If there is only one argument, it must be a dictionary mapping
   Unicode ordinals (integers) or characters (strings of length 1) to
   Unicode ordinals, strings (of arbitrary lengths) or "None".
   Character keys will then be converted to ordinals.

   If there are two arguments, they must be strings of equal length,
   and in the resulting dictionary, each character in x will be mapped
   to the character at the same position in y.  If there is a third
   argument, it must be a string, whose characters will be mapped to
   "None" in the result.

str.partition(sep)

   Split the string at the first occurrence of *sep*, and return a
   3-tuple containing the part before the separator, the separator
   itself, and the part after the separator.  If the separator is not
   found, return a 3-tuple containing the string itself, followed by
   two empty strings.

str.removeprefix(prefix, /)

   If the string starts with the *prefix* string, return
   "string[len(prefix):]". Otherwise, return a copy of the original
   string:

      >>> 'TestHook'.removeprefix('Test')
      'Hook'
      >>> 'BaseTestCase'.removeprefix('Test')
      'BaseTestCase'

   Added in version 3.9.

str.removesuffix(suffix, /)

   If the string ends with the *suffix* string and that *suffix* is
   not empty, return "string[:-len(suffix)]". Otherwise, return a copy
   of the original string:

      >>> 'MiscTests'.removesuffix('Tests')
      'Misc'
      >>> 'TmpDirMixin'.removesuffix('Tests')
      'TmpDirMixin'

   Added in version 3.9.

str.replace(old, new, count=-1)

   Return a copy of the string with all occurrences of substring *old*
   replaced by *new*.  If *count* is given, only the first *count*
   occurrences are replaced. If *count* is not specified or "-1", then
   all occurrences are replaced.

   Changed in version 3.13: *count* is now supported as a keyword
   argument.

str.rfind(sub[, start[, end]])

   Return the highest index in the string where substring *sub* is
   found, such that *sub* is contained within "s[start:end]".
   Optional arguments *start* and *end* are interpreted as in slice
   notation.  Return "-1" on failure.

str.rindex(sub[, start[, end]])

   Like "rfind()" but raises "ValueError" when the substring *sub* is
   not found.

str.rjust(width[, fillchar])

   Return the string right justified in a string of length *width*.
   Padding is done using the specified *fillchar* (default is an ASCII
   space). The original string is returned if *width* is less than or
   equal to "len(s)".

str.rpartition(sep)

   Split the string at the last occurrence of *sep*, and return a
   3-tuple containing the part before the separator, the separator
   itself, and the part after the separator.  If the separator is not
   found, return a 3-tuple containing two empty strings, followed by
   the string itself.

str.rsplit(sep=None, maxsplit=-1)

   Return a list of the words in the string, using *sep* as the
   delimiter string. If *maxsplit* is given, at most *maxsplit* splits
   are done, the *rightmost* ones.  If *sep* is not specified or
   "None", any whitespace string is a separator.  Except for splitting
   from the right, "rsplit()" behaves like "split()" which is
   described in detail below.

str.rstrip([chars])

   Return a copy of the string with trailing characters removed.  The
   *chars* argument is a string specifying the set of characters to be
   removed.  If omitted or "None", the *chars* argument defaults to
   removing whitespace.  The *chars* argument is not a suffix; rather,
   all combinations of its values are stripped:

      >>> '   spacious   '.rstrip()
      '   spacious'
      >>> 'mississippi'.rstrip('ipz')
      'mississ'

   See "str.removesuffix()" for a method that will remove a single
   suffix string rather than all of a set of characters.  For example:

      >>> 'Monty Python'.rstrip(' Python')
      'M'
      >>> 'Monty Python'.removesuffix(' Python')
      'Monty'

str.split(sep=None, maxsplit=-1)

   Return a list of the words in the string, using *sep* as the
   delimiter string.  If *maxsplit* is given, at most *maxsplit*
   splits are done (thus, the list will have at most "maxsplit+1"
   elements).  If *maxsplit* is not specified or "-1", then there is
   no limit on the number of splits (all possible splits are made).

   If *sep* is given, consecutive delimiters are not grouped together
   and are deemed to delimit empty strings (for example,
   "'1,,2'.split(',')" returns "['1', '', '2']").  The *sep* argument
   may consist of multiple characters as a single delimiter (to split
   with multiple delimiters, use "re.split()"). Splitting an empty
   string with a specified separator returns "['']".

   For example:

      >>> '1,2,3'.split(',')
      ['1', '2', '3']
      >>> '1,2,3'.split(',', maxsplit=1)
      ['1', '2,3']
      >>> '1,2,,3,'.split(',')
      ['1', '2', '', '3', '']
      >>> '1<>2<>3<4'.split('<>')
      ['1', '2', '3<4']

   If *sep* is not specified or is "None", a different splitting
   algorithm is applied: runs of consecutive whitespace are regarded
   as a single separator, and the result will contain no empty strings
   at the start or end if the string has leading or trailing
   whitespace.  Consequently, splitting an empty string or a string
   consisting of just whitespace with a "None" separator returns "[]".

   For example:

      >>> '1 2 3'.split()
      ['1', '2', '3']
      >>> '1 2 3'.split(maxsplit=1)
      ['1', '2 3']
      >>> '   1   2   3   '.split()
      ['1', '2', '3']

   If *sep* is not specified or is "None" and  *maxsplit* is "0", only
   leading runs of consecutive whitespace are considered.

   For example:

      >>> "".split(None, 0)
      []
      >>> "   ".split(None, 0)
      []
      >>> "   foo   ".split(maxsplit=0)
      ['foo   ']

str.splitlines(keepends=False)

   Return a list of the lines in the string, breaking at line
   boundaries.  Line breaks are not included in the resulting list
   unless *keepends* is given and true.

   This method splits on the following line boundaries.  In
   particular, the boundaries are a superset of *universal newlines*.

   +-------------------------+-------------------------------+
   | Representation          | Description                   |
   |=========================|===============================|
   | "\n"                    | Line Feed                     |
   +-------------------------+-------------------------------+
   | "\r"                    | Carriage Return               |
   +-------------------------+-------------------------------+
   | "\r\n"                  | Carriage Return + Line Feed   |
   +-------------------------+-------------------------------+
   | "\v" or "\x0b"          | Line Tabulation               |
   +-------------------------+-------------------------------+
   | "\f" or "\x0c"          | Form Feed                     |
   +-------------------------+-------------------------------+
   | "\x1c"                  | File Separator                |
   +-------------------------+-------------------------------+
   | "\x1d"                  | Group Separator               |
   +-------------------------+-------------------------------+
   | "\x1e"                  | Record Separator              |
   +-------------------------+-------------------------------+
   | "\x85"                  | Next Line (C1 Control Code)   |
   +-------------------------+-------------------------------+
   | "\u2028"                | Line Separator                |
   +-------------------------+-------------------------------+
   | "\u2029"                | Paragraph Separator           |
   +-------------------------+-------------------------------+

   Changed in version 3.2: "\v" and "\f" added to list of line
   boundaries.

   For example:

      >>> 'ab c\n\nde fg\rkl\r\n'.splitlines()
      ['ab c', '', 'de fg', 'kl']
      >>> 'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
      ['ab c\n', '\n', 'de fg\r', 'kl\r\n']

   Unlike "split()" when a delimiter string *sep* is given, this
   method returns an empty list for the empty string, and a terminal
   line break does not result in an extra line:

      >>> "".splitlines()
      []
      >>> "One line\n".splitlines()
      ['One line']

   For comparison, "split('\n')" gives:

      >>> ''.split('\n')
      ['']
      >>> 'Two lines\n'.split('\n')
      ['Two lines', '']

str.startswith(prefix[, start[, end]])

   Return "True" if string starts with the *prefix*, otherwise return
   "False". *prefix* can also be a tuple of prefixes to look for.
   With optional *start*, test string beginning at that position.
   With optional *end*, stop comparing string at that position.

str.strip([chars])

   Return a copy of the string with the leading and trailing
   characters removed. The *chars* argument is a string specifying the
   set of characters to be removed. If omitted or "None", the *chars*
   argument defaults to removing whitespace. The *chars* argument is
   not a prefix or suffix; rather, all combinations of its values are
   stripped:

      >>> '   spacious   '.strip()
      'spacious'
      >>> 'www.example.com'.strip('cmowz.')
      'example'

   The outermost leading and trailing *chars* argument values are
   stripped from the string. Characters are removed from the leading
   end until reaching a string character that is not contained in the
   set of characters in *chars*. A similar action takes place on the
   trailing end. For example:

      >>> comment_string = '#....... Section 3.2.1 Issue #32 .......'
      >>> comment_string.strip('.#! ')
      'Section 3.2.1 Issue #32'

str.swapcase()

   Return a copy of the string with uppercase characters converted to
   lowercase and vice versa. Note that it is not necessarily true that
   "s.swapcase().swapcase() == s".

str.title()

   Return a titlecased version of the string where words start with an
   uppercase character and the remaining characters are lowercase.

   For example:

      >>> 'Hello world'.title()
      'Hello World'

   The algorithm uses a simple language-independent definition of a
   word as groups of consecutive letters.  The definition works in
   many contexts but it means that apostrophes in contractions and
   possessives form word boundaries, which may not be the desired
   result:

      >>> "they're bill's friends from the UK".title()
      "They'Re Bill'S Friends From The Uk"

   The "string.capwords()" function does not have this problem, as it
   splits words on spaces only.

   Alternatively, a workaround for apostrophes can be constructed
   using regular expressions:

      >>> import re
      >>> def titlecase(s):
      ...     return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
      ...                   lambda mo: mo.group(0).capitalize(),
      ...                   s)
      ...
      >>> titlecase("they're bill's friends.")
      "They're Bill's Friends."

str.translate(table)

   Return a copy of the string in which each character has been mapped
   through the given translation table.  The table must be an object
   that implements indexing via "__getitem__()", typically a *mapping*
   or *sequence*.  When indexed by a Unicode ordinal (an integer), the
   table object can do any of the following: return a Unicode ordinal
   or a string, to map the character to one or more other characters;
   return "None", to delete the character from the return string; or
   raise a "LookupError" exception, to map the character to itself.

   You can use "str.maketrans()" to create a translation map from
   character-to-character mappings in different formats.

   See also the "codecs" module for a more flexible approach to custom
   character mappings.

str.upper()

   Return a copy of the string with all the cased characters [4]
   converted to uppercase.  Note that "s.upper().isupper()" might be
   "False" if "s" contains uncased characters or if the Unicode
   category of the resulting character(s) is not “Lu” (Letter,
   uppercase), but e.g. “Lt” (Letter, titlecase).

   The uppercasing algorithm used is described in section 3.13
   ‘Default Case Folding’ of the Unicode Standard.

str.zfill(width)

   Return a copy of the string left filled with ASCII "'0'" digits to
   make a string of length *width*. A leading sign prefix
   ("'+'"/"'-'") is handled by inserting the padding *after* the sign
   character rather than before. The original string is returned if
   *width* is less than or equal to "len(s)".

   For example:

      >>> "42".zfill(5)
      '00042'
      >>> "-42".zfill(5)
      '-0042'
