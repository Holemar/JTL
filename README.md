# JTL
[简体中文版本](./README_CN.md)  
JSON Transformation Language, JTL, is like `sed` and `awk` for JSON: a simple language for
transforming JSON values into other JSON values. The syntax of the language itself is also JSON
(so it can operate on itself - meta!). Command line prototyping is easy:

    > cat tests/faa1.json
    {
        ...
        "weather": {
            ...,
            "temp": "66.0 F (18.9 C)",
            ...
        }
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp"}'
    {
        "tempF": "66.0 F (18.9 C)"
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words"}'
    {
        "tempF": [
            "66.0",
            "F",
            "(18.9",
            "C)"
        ]
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words $ first"}'
    {
        "tempF": "66.0"
    }

    > cat tests/faa1.json | ./JTL/__init__.py '{"tempF": "weather.temp $ words $ first $ toFloat"}'
    {
        "tempF": 66.0
    }

## Motivation
Although JSON has replaced XML as the de facto data format for structured text data, no standard suite of
supporting technologies has emerged. JTL is to JSON what XSL is to XML -- a transformation language written
in the underlying format. It allows the quick creation of format converters, adapters for 3rd party API's,
transform scripts for ETL's, and more.

JTL is designed to be simple to parse for both humans and computers. This makes the implementation simple,
and allows the creation of value-added features like query optimizers.

Because it's input and output are JSON, it's highly composable. In fact, sometimes composition is the only
way to do things. Since the code is also JSON, it can even be used self-referentially, for example to
automate refactoring.

## Syntax
The basic syntax of a JTL transformation is a JSON dictionary with the same structure as the output, where all  values are strings are JTL expressions.

JTL expressions are of the form `<SELECTOR> [$ <FUNCTION> <ARG1>*]*`.

Selectors are `.` separated paths: for example, `a.b.c` would return `3` from `{"a": {"b": {"c": 3}}}`.

Functions (and operators) transform data extracted by selectors.

## Operators
JTL supports the following operators in [Polish notation](https://en.wikipedia.org/wiki/Polish_notation) with the same semantics as Python:

* Arithmetic: `+`, `-`, `*`, `/`, `**`, `%`
* Comparison: `==`, `!=`, `<`, `<=`, `>`, `>=`

For example:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.temp $ words $ first $ toFloat $ + 3.0 $ / 23"}'
    {
        "x": 3.0
    }

## Functions
JTL has a wide variety of built in transformations. In order to easily handle missing values, all functions will pass through null unless otherwise indicated (much like an option monad).

### Basic

#### `default <VALUE>`
Returns the input value or the first argument if the input is `null` (this is the one case with special `null` handling).

#### `defaultNan`
Returns the input value or `NaN` if the input is `null`.

#### `isNull`
Returns true if the value is `null`.

#### `toBool`
Converts the input value to a `boolean`.

#### `toFloat`
Converts the input value to a float, returning `null` if it is not a valid number.

#### `toInt`
Converts the input value to an integer, returning `null` if it is not a valid integer.

#### `toNumber`
Converts the input value to an integer or float, returning `null` if it is not a valid number.

#### `toString`
Converts the input value to a string.

#### `null`
Always return `null`.


### Bool

* `not`: Inverts the boolean value.
* `and`: All values are `true`.
* `or`: One of the values is `true`.

### Dictionary

#### `keys`
Returns the keys of the dictionary as a list.

#### `values`
Returns the values of the dictionary as a list.

#### `enumChange`
Returns the value of the enum.  
JTL expressions: `<SELECTOR> $ enumChange '{"F": "female", "M": "male"}'`  

For example:

```python
from JTL import Interpreter

data = {
    'a': {
        'X': 3,
        'Y': 2
    }
}
result = Interpreter.transform(data, '''a.Y $ enumChange "{1: 'one', 2: 'two'}" ''')
print(result)  # print: two
```

#### `enumFileChange`
Returns the value of the enum. And the enum json load by a file.  
JTL expressions: `<SELECTOR> $ enumFileChange file_path`  
The file path can be either absolute addresses or relative to the project startup directory.

For example:

```python
from JTL import Interpreter

data = {
    'a': {
        'X': 3,
        'Y': 2
    }
}
result = Interpreter.transform(data, 'a.Y $ enumFileChange "/data/example_enum.json" ')
```

### Hashing
JTL supports a variety of cryptographic hash functions: `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`. In addition, [HMAC's](https://en.wikipedia.org/wiki/Hash-based_message_authentication_code) are supported for each of these hash types (e.g. `hmac_md5`).

### Math

* Basics: `abs`, `ceil`, `floor`
* Exponentials: `exp`, `lg`, `ln`, `log`, `sqrt`
* Flags: `isFinite`, `isNan`
* Trigonometry: `sin`, `cos`, `tan`
* Hyperbolic trigonometry: `sinh`, `cosh`, `tanh`
* Advanced: `erf`

### Sequence

#### `index number`
Returns the value by the index number the element appears in the list.

#### `count <ELEMENT>`
Returns the number of times the element appears in the list.

#### `first`
Returns the first element of the list, or `null` if the list is empty.

#### `last`
Returns the last element of the list, or `null` if the list is empty.

#### `rmFirst`
Returns the rest of the list after the first element.

#### `rmLast`
Returns all of the elements of the list except the last one.

#### `rmNull`
Returns all of the elements of the list except the `null` element.

#### `list`
Returns all of the parameter values as a list except the first value.

For example:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "* $ list weather.temp 1 \"ab\" city" }'
    {
        "x": ["66.0 F (18.9 C)", 1, "ab", "Washington"]
    }

##### return more fields to a list

```python
from JTL import Interpreter

data = {
    "skill_type": "english",
    "compet_level": "four level",
    "time_use": "three years"
}
result = Interpreter.transform(data, '* $ list skill_type compet_level time_use ')
print(result)  # ['english', 'four level', 'three years']
```


##### concat more fields to one

```python
from JTL import Interpreter

data = {
    "skill_type": "english",
    "compet_level": "four level",
    "time_use": "three years"
}
result = Interpreter.transform(data, '* $ list skill_type compet_level time_use $ join "/" ')
print(result)  # english/four level/three years
```


##### get the first not null value in more fields

```python
from JTL import Interpreter

data = {
    "INTENTION_PLACE": None,
    "INTENTION_PLACE_ONE": "London",
    "INTENTION_PLACE_TWO": "Washington"
}
result = Interpreter.transform(data, '* $ list INTENTION_PLACE, INTENTION_PLACE_ONE, INTENTION_PLACE_TWO $ rmNull $ first')
print(result)  # London
```

#### `length`
Returns the length of the list.

#### `max`
Finds the maximum value in the list.

#### `min`
Finds the minimum value in the list.

#### `sorted`
Returns a sorted version of the list.

#### `sum`
Takes the sum of values in the list.

#### `unique`
Returns a copy of the list with duplicates removed.

### String

* Case transformation: `capitalize`, `lower`, `swapCase`, `upper`
* Search: `find`, `replace`, `startsWith`, `endsWith`
* Split / join: `join`, `split`, `lines`, `unlines`, `words`, `unwords`
* Whitespace: `lstrip`, `rstrip`, `strip`

### date/time

#### Converts date/time to a string `toString`
Converts the value of type `datetime.datetime`, `time` to a string as format `%Y-%m-%dT%H:%M:%S`.  
Converts the value of type `datetime.date` to a string as format `%Y-%m-%d`.  
Converts the value of type `datetime.time` to a string as format `%H:%M:%S`.  
JTL expressions: `<SELECTOR> $ toString`  

#### Converts date to a string `dateToString`
Converts the value to a date string as default format `%Y-%m-%d`.  
The first parameter is string format.  
The second parameter bool `default_now`: True: when value is `null` regard as now, False: when value is `null` regard as `null`.  
JTL expressions: `<SELECTOR> $ dateToString "<format_str>"? default_now?`  

#### Converts time to a string `datetimeToString`
Converts the value to a datetime string as default format `%Y-%m-%dT%H:%M:%S`.  
The first parameter is string format.  
The second parameter bool `default_now`: True: when value is `null` regard as now, False: when value is `null` regard as `null`.  
JTL expressions: `<SELECTOR> $ datetimeToString "<format_str>"? default_now?`  

#### Converts input value to date `toDate`
Converts the value to a date of type `datetime.date`.  
The first parameter bool `default_now`: True: when value is `null` regard as now, False: when value is `null` regard as `null`.  
The second parameter string format, when input value is a string, set the from format string.
JTL expressions: `<SELECTOR> $ toDate default_now? "<from_format_str>"? `  

#### Converts input value to datetime `toDatetime`
Converts the value to a datetime of type `datetime.datetime`.  
The first parameter bool `default_now`: True: when value is `null` regard as now, False: when value is `null` regard as `null`.  
The second parameter string format, when input value is a string, set the from format string.
JTL expressions: `<SELECTOR> $ toDatetime default_now? "<from_format_str>"? `  

#### Count age by birthday `countAge`
