# Python Language Reference: Lexical Analysis

Source URL: https://docs.python.org/3.13/reference/lexical_analysis.html
Reference version: Python 3.13
Licence: Python Software Foundation License Version 2 (https://docs.python.org/3.13/license.html)
Local extraction: CPython 3.13 pydoc_data.topics generated from the official documentation

### TOPIC: identifiers
Identifiers and keywords
************************

Identifiers (also referred to as *names*) are described by the
following lexical definitions.

The syntax of identifiers in Python is based on the Unicode standard
annex UAX-31, with elaboration and changes as defined below; see also
**PEP 3131** for further details.

Within the ASCII range (U+0001..U+007F), the valid characters for
identifiers include the uppercase and lowercase letters "A" through
"Z", the underscore "_" and, except for the first character, the
digits "0" through "9". Python 3.0 introduced additional characters
from outside the ASCII range (see **PEP 3131**).  For these
characters, the classification uses the version of the Unicode
Character Database as included in the "unicodedata" module.

Identifiers are unlimited in length.  Case is significant.

   identifier   ::= xid_start xid_continue*
   id_start     ::= <all characters in general categories Lu, Ll, Lt, Lm, Lo, Nl, the underscore, and characters with the Other_ID_Start property>
   id_continue  ::= <all characters in id_start, plus characters in the categories Mn, Mc, Nd, Pc and others with the Other_ID_Continue property>
   xid_start    ::= <all characters in id_start whose NFKC normalization is in "id_start xid_continue*">
   xid_continue ::= <all characters in id_continue whose NFKC normalization is in "id_continue*">

The Unicode category codes mentioned above stand for:

* *Lu* - uppercase letters

* *Ll* - lowercase letters

* *Lt* - titlecase letters

* *Lm* - modifier letters

* *Lo* - other letters

* *Nl* - letter numbers

* *Mn* - nonspacing marks

* *Mc* - spacing combining marks

* *Nd* - decimal numbers

* *Pc* - connector punctuations

* *Other_ID_Start* - explicit list of characters in PropList.txt to
  support backwards compatibility

* *Other_ID_Continue* - likewise

All identifiers are converted into the normal form NFKC while parsing;
comparison of identifiers is based on NFKC.

A non-normative HTML file listing all valid identifier characters for
Unicode 15.1.0 can be found at
https://www.unicode.org/Public/15.1.0/ucd/DerivedCoreProperties.txt


Keywords
========

The following identifiers are used as reserved words, or *keywords* of
the language, and cannot be used as ordinary identifiers.  They must
be spelled exactly as written here:

   False      await      else       import     pass
   None       break      except     in         raise
   True       class      finally    is         return
   and        continue   for        lambda     try
   as         def        from       nonlocal   while
   assert     del        global     not        with
   async      elif       if         or         yield


Soft Keywords
=============

Added in version 3.10.

Some identifiers are only reserved under specific contexts. These are
known as *soft keywords*.  The identifiers "match", "case", "type" and
"_" can syntactically act as keywords in certain contexts, but this
distinction is done at the parser level, not when tokenizing.

As soft keywords, their use in the grammar is possible while still
preserving compatibility with existing code that uses these names as
identifier names.

"match", "case", and "_" are used in the "match" statement. "type" is
used in the "type" statement.

Changed in version 3.12: "type" is now a soft keyword.


Reserved classes of identifiers
===============================

Certain classes of identifiers (besides keywords) have special
meanings.  These classes are identified by the patterns of leading and
trailing underscore characters:

"_*"
   Not imported by "from module import *".

"_"
   In a "case" pattern within a "match" statement, "_" is a soft
   keyword that denotes a wildcard.

   Separately, the interactive interpreter makes the result of the
   last evaluation available in the variable "_". (It is stored in the
   "builtins" module, alongside built-in functions like "print".)

   Elsewhere, "_" is a regular identifier. It is often used to name
   “special” items, but it is not special to Python itself.

   Note:

     The name "_" is often used in conjunction with
     internationalization; refer to the documentation for the
     "gettext" module for more information on this convention.It is
     also commonly used for unused variables.

"__*__"
   System-defined names, informally known as “dunder” names. These
   names are defined by the interpreter and its implementation
   (including the standard library). Current system names are
   discussed in the Special method names section and elsewhere. More
   will likely be defined in future versions of Python.  *Any* use of
   "__*__" names, in any context, that does not follow explicitly
   documented use, is subject to breakage without warning.

"__*"
   Class-private names.  Names in this category, when used within the
   context of a class definition, are re-written to use a mangled form
   to help avoid name clashes between “private” attributes of base and
   derived classes. See section Identifiers (Names).

### TOPIC: id-classes
Reserved classes of identifiers
*******************************

Certain classes of identifiers (besides keywords) have special
meanings.  These classes are identified by the patterns of leading and
trailing underscore characters:

"_*"
   Not imported by "from module import *".

"_"
   In a "case" pattern within a "match" statement, "_" is a soft
   keyword that denotes a wildcard.

   Separately, the interactive interpreter makes the result of the
   last evaluation available in the variable "_". (It is stored in the
   "builtins" module, alongside built-in functions like "print".)

   Elsewhere, "_" is a regular identifier. It is often used to name
   “special” items, but it is not special to Python itself.

   Note:

     The name "_" is often used in conjunction with
     internationalization; refer to the documentation for the
     "gettext" module for more information on this convention.It is
     also commonly used for unused variables.

"__*__"
   System-defined names, informally known as “dunder” names. These
   names are defined by the interpreter and its implementation
   (including the standard library). Current system names are
   discussed in the Special method names section and elsewhere. More
   will likely be defined in future versions of Python.  *Any* use of
   "__*__" names, in any context, that does not follow explicitly
   documented use, is subject to breakage without warning.

"__*"
   Class-private names.  Names in this category, when used within the
   context of a class definition, are re-written to use a mangled form
   to help avoid name clashes between “private” attributes of base and
   derived classes. See section Identifiers (Names).

### TOPIC: strings
String and Bytes literals
*************************

String literals are described by the following lexical definitions:

   stringliteral   ::= [stringprefix](shortstring | longstring)
   stringprefix    ::= "r" | "u" | "R" | "U" | "f" | "F"
                       | "fr" | "Fr" | "fR" | "FR" | "rf" | "rF" | "Rf" | "RF"
   shortstring     ::= "'" shortstringitem* "'" | '"' shortstringitem* '"'
   longstring      ::= "'''" longstringitem* "'''" | '"""' longstringitem* '"""'
   shortstringitem ::= shortstringchar | stringescapeseq
   longstringitem  ::= longstringchar | stringescapeseq
   shortstringchar ::= <any source character except "\" or newline or the quote>
   longstringchar  ::= <any source character except "\">
   stringescapeseq ::= "\" <any source character>

   bytesliteral   ::= bytesprefix(shortbytes | longbytes)
   bytesprefix    ::= "b" | "B" | "br" | "Br" | "bR" | "BR" | "rb" | "rB" | "Rb" | "RB"
   shortbytes     ::= "'" shortbytesitem* "'" | '"' shortbytesitem* '"'
   longbytes      ::= "'''" longbytesitem* "'''" | '"""' longbytesitem* '"""'
   shortbytesitem ::= shortbyteschar | bytesescapeseq
   longbytesitem  ::= longbyteschar | bytesescapeseq
   shortbyteschar ::= <any ASCII character except "\" or newline or the quote>
   longbyteschar  ::= <any ASCII character except "\">
   bytesescapeseq ::= "\" <any ASCII character>

One syntactic restriction not indicated by these productions is that
whitespace is not allowed between the "stringprefix" or "bytesprefix"
and the rest of the literal. The source character set is defined by
the encoding declaration; it is UTF-8 if no encoding declaration is
given in the source file; see section Encoding declarations.

In plain English: Both types of literals can be enclosed in matching
single quotes ("'") or double quotes (""").  They can also be enclosed
in matching groups of three single or double quotes (these are
generally referred to as *triple-quoted strings*). The backslash ("\")
character is used to give special meaning to otherwise ordinary
characters like "n", which means ‘newline’ when escaped ("\n"). It can
also be used to escape characters that otherwise have a special
meaning, such as newline, backslash itself, or the quote character.
See escape sequences below for examples.

Bytes literals are always prefixed with "'b'" or "'B'"; they produce
an instance of the "bytes" type instead of the "str" type.  They may
only contain ASCII characters; bytes with a numeric value of 128 or
greater must be expressed with escapes.

Both string and bytes literals may optionally be prefixed with a
letter "'r'" or "'R'"; such constructs are called *raw string
literals* and *raw bytes literals* respectively and treat backslashes
as literal characters.  As a result, in raw string literals, "'\U'"
and "'\u'" escapes are not treated specially.

Added in version 3.3: The "'rb'" prefix of raw bytes literals has been
added as a synonym of "'br'".Support for the unicode legacy literal
("u'value'") was reintroduced to simplify the maintenance of dual
Python 2.x and 3.x codebases. See **PEP 414** for more information.

A string literal with "'f'" or "'F'" in its prefix is a *formatted
string literal*; see f-strings.  The "'f'" may be combined with "'r'",
but not with "'b'" or "'u'", therefore raw formatted strings are
possible, but formatted bytes literals are not.

In triple-quoted literals, unescaped newlines and quotes are allowed
(and are retained), except that three unescaped quotes in a row
terminate the literal.  (A “quote” is the character used to open the
literal, i.e. either "'" or """.)


Escape sequences
================

Unless an "'r'" or "'R'" prefix is present, escape sequences in string
and bytes literals are interpreted according to rules similar to those
used by Standard C.  The recognized escape sequences are:

+---------------------------+-----------------------------------+---------+
| Escape Sequence           | Meaning                           | Notes   |
|===========================|===================================|=========|
| "\"<newline>              | Backslash and newline ignored     | (1)     |
+---------------------------+-----------------------------------+---------+
| "\\"                      | Backslash ("\")                   |         |
+---------------------------+-----------------------------------+---------+
| "\'"                      | Single quote ("'")                |         |
+---------------------------+-----------------------------------+---------+
| "\""                      | Double quote (""")                |         |
+---------------------------+-----------------------------------+---------+
| "\a"                      | ASCII Bell (BEL)                  |         |
+---------------------------+-----------------------------------+---------+
| "\b"                      | ASCII Backspace (BS)              |         |
+---------------------------+-----------------------------------+---------+
| "\f"                      | ASCII Formfeed (FF)               |         |
+---------------------------+-----------------------------------+---------+
| "\n"                      | ASCII Linefeed (LF)               |         |
+---------------------------+-----------------------------------+---------+
| "\r"                      | ASCII Carriage Return (CR)        |         |
+---------------------------+-----------------------------------+---------+
| "\t"                      | ASCII Horizontal Tab (TAB)        |         |
+---------------------------+-----------------------------------+---------+
| "\v"                      | ASCII Vertical Tab (VT)           |         |
+---------------------------+-----------------------------------+---------+
| "\*ooo*"                  | Character with octal value *ooo*  | (2,4)   |
+---------------------------+-----------------------------------+---------+
| "\x*hh*"                  | Character with hex value *hh*     | (3,4)   |
+---------------------------+-----------------------------------+---------+

Escape sequences only recognized in string literals are:

+---------------------------+-----------------------------------+---------+
| Escape Sequence           | Meaning                           | Notes   |
|===========================|===================================|=========|
| "\N{*name*}"              | Character named *name* in the     | (5)     |
|                           | Unicode database                  |         |
+---------------------------+-----------------------------------+---------+
| "\u*xxxx*"                | Character with 16-bit hex value   | (6)     |
|                           | *xxxx*                            |         |
+---------------------------+-----------------------------------+---------+
| "\U*xxxxxxxx*"            | Character with 32-bit hex value   | (7)     |
|                           | *xxxxxxxx*                        |         |
+---------------------------+-----------------------------------+---------+

Notes:

1. A backslash can be added at the end of a line to ignore the
   newline:

      >>> 'This string will not include \
      ... backslashes or newline characters.'
      'This string will not include backslashes or newline characters.'

   The same result can be achieved using triple-quoted strings, or
   parentheses and string literal concatenation.

2. As in Standard C, up to three octal digits are accepted.

   Changed in version 3.11: Octal escapes with value larger than
   "0o377" produce a "DeprecationWarning".

   Changed in version 3.12: Octal escapes with value larger than
   "0o377" produce a "SyntaxWarning". In a future Python version they
   will be eventually a "SyntaxError".

3. Unlike in Standard C, exactly two hex digits are required.

4. In a bytes literal, hexadecimal and octal escapes denote the byte
   with the given value. In a string literal, these escapes denote a
   Unicode character with the given value.

5. Changed in version 3.3: Support for name aliases [1] has been
   added.

6. Exactly four hex digits are required.

7. Any Unicode character can be encoded this way.  Exactly eight hex
   digits are required.

Unlike Standard C, all unrecognized escape sequences are left in the
string unchanged, i.e., *the backslash is left in the result*.  (This
behavior is useful when debugging: if an escape sequence is mistyped,
the resulting output is more easily recognized as broken.)  It is also
important to note that the escape sequences only recognized in string
literals fall into the category of unrecognized escapes for bytes
literals.

Changed in version 3.6: Unrecognized escape sequences produce a
"DeprecationWarning".

Changed in version 3.12: Unrecognized escape sequences produce a
"SyntaxWarning". In a future Python version they will be eventually a
"SyntaxError".

Even in a raw literal, quotes can be escaped with a backslash, but the
backslash remains in the result; for example, "r"\""" is a valid
string literal consisting of two characters: a backslash and a double
quote; "r"\"" is not a valid string literal (even a raw string cannot
end in an odd number of backslashes).  Specifically, *a raw literal
cannot end in a single backslash* (since the backslash would escape
the following quote character).  Note also that a single backslash
followed by a newline is interpreted as those two characters as part
of the literal, *not* as a line continuation.

### TOPIC: numbers
Numeric literals
****************

There are three types of numeric literals: integers, floating-point
numbers, and imaginary numbers.  There are no complex literals
(complex numbers can be formed by adding a real number and an
imaginary number).

Note that numeric literals do not include a sign; a phrase like "-1"
is actually an expression composed of the unary operator ‘"-"’ and the
literal "1".

### TOPIC: integers
Integer literals
****************

Integer literals are described by the following lexical definitions:

   integer      ::= decinteger | bininteger | octinteger | hexinteger
   decinteger   ::= nonzerodigit (["_"] digit)* | "0"+ (["_"] "0")*
   bininteger   ::= "0" ("b" | "B") (["_"] bindigit)+
   octinteger   ::= "0" ("o" | "O") (["_"] octdigit)+
   hexinteger   ::= "0" ("x" | "X") (["_"] hexdigit)+
   nonzerodigit ::= "1"..."9"
   digit        ::= "0"..."9"
   bindigit     ::= "0" | "1"
   octdigit     ::= "0"..."7"
   hexdigit     ::= digit | "a"..."f" | "A"..."F"

There is no limit for the length of integer literals apart from what
can be stored in available memory.

Underscores are ignored for determining the numeric value of the
literal.  They can be used to group digits for enhanced readability.
One underscore can occur between digits, and after base specifiers
like "0x".

Note that leading zeros in a non-zero decimal number are not allowed.
This is for disambiguation with C-style octal literals, which Python
used before version 3.0.

Some examples of integer literals:

   7     2147483647                        0o177    0b100110111
   3     79228162514264337593543950336     0o377    0xdeadbeef
         100_000_000_000                   0b_1110_0101

Changed in version 3.6: Underscores are now allowed for grouping
purposes in literals.

### TOPIC: floating
Floating-point literals
***********************

Floating-point literals are described by the following lexical
definitions:

   floatnumber   ::= pointfloat | exponentfloat
   pointfloat    ::= [digitpart] fraction | digitpart "."
   exponentfloat ::= (digitpart | pointfloat) exponent
   digitpart     ::= digit (["_"] digit)*
   fraction      ::= "." digitpart
   exponent      ::= ("e" | "E") ["+" | "-"] digitpart

Note that the integer and exponent parts are always interpreted using
radix 10. For example, "077e010" is legal, and denotes the same number
as "77e10". The allowed range of floating-point literals is
implementation-dependent.  As in integer literals, underscores are
supported for digit grouping.

Some examples of floating-point literals:

   3.14    10.    .001    1e100    3.14e-10    0e0    3.14_15_93

Changed in version 3.6: Underscores are now allowed for grouping
purposes in literals.

### TOPIC: imaginary
Imaginary literals
******************

Imaginary literals are described by the following lexical definitions:

   imagnumber ::= (floatnumber | digitpart) ("j" | "J")

An imaginary literal yields a complex number with a real part of 0.0.
Complex numbers are represented as a pair of floating-point numbers
and have the same restrictions on their range.  To create a complex
number with a nonzero real part, add a floating-point number to it,
e.g., "(3+4j)".  Some examples of imaginary literals:

   3.14j   10.j    10j     .001j   1e100j   3.14e-10j   3.14_15_93j
