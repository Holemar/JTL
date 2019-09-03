# JTL
JSON Transformation Language, JTL, 是一个像 `sed` 和 `awk` 的 JSON 解析器。
是一个简单的 json 转换语言，容易得像如下语句：

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


## 动机
虽然 JSON 已经取代XML作为结构化文本数据的事实上的数据格式，但还没有出现标准支持技术。
JTL 是 JSON 的 XSL（一种 XML 的底层转换语言格式）。
它允许快速创建格式转换器，第三方API的适配器，转换ETL的脚本等等。

JTL旨在简单地被人和计算机使用。 这使得实现简单，并允许创建像查询优化器这样的增值功能。

因为它的输入和输出是JSON，所以它是高度可组合的。 事实上，有时组合是唯一的做事的方式。
由于输入和输出都是JSON，它甚至可以自我引用，例如自动化重构。

## 语法
JTL转换的基本语法是与输出结构相同的JSON字典，其中所有值都被看做是字符串的JTL表达式。

JTL表达式的形式为`<SELECTOR> [$ <FUNCTION> <ARG1> *]*`。

选择器是`.`分隔的路径：例如，`a.b.c`将从`{"a": {"b": {"c": 3}}}`中返回`3`。

函数（和运算符）转换由选择器提取的数据。

## 操作符
JTL 简易得像用python一样支持这地址里面的所有操作符 [Polish符号](https://en.wikipedia.org/wiki/Polish_notation):

* 算术运算符: `+`, `-`, `*`, `/`, `**`, `%`
* 对比符: `==`, `!=`, `<`, `<=`, `>`, `>=`

如:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.temp $ words $ first $ toFloat $ + 3.0 $ / 23"}'
    {
        "x": 3.0
    }

## 函数
JTL 具有各种宽松的内置转换函数，可以轻松处理缺失值，除非另有说明，否则所有函数都将可以处理null值（就像monad）。

### 基础函数

#### `default <VALUE>`
如果传入值是 `null`，将返回指定的 `<VALUE>` 值。否则返回传入值。

如:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.spring $ default 'one' ", "y": "weather.temp $ default weather.temp "}'
    {
        "x": "one",
        "y": "66.0 F (18.9 C)"
    }

#### `defaultNan`
如果传入值是`null`，则返回`NaN`。

#### `isNull`
判断传入值是否为`null`。

#### `toBool`
将输入值转成布尔(boolean)值。

#### `toFloat`
将输入值转成 float 值。如果传入值不是合法的数值则返回`null`。

#### `toInt`
将输入值转成 int 值。如果传入值不是合法的数值则返回`null`。

#### `toString`
将输入值转成字符串。

### Bool

* not: 反转布尔值。
* and: 所有值都是 真 时返回 True, 否则返回 False.
* or: 其中一个值是 真 时返回 True, 所有值都是 假 时返回 False.

### Dictionary

#### `keys`
返回字典的 keys 列表。

#### `values`
返回字典的 values 列表。

#### `enumChange`
返回枚举dict对应的值。

如:

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
返回枚举dict对应的值。但输入的参数是文件路径，从文件中读取枚举dict。一般在枚举很大时用。

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

#### `索引值`
返回列表里面指定索引位置的值，当索引下标越界时返回 `null`。 下标从 0 开始。

如:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.temp $ words $ 1"}'
    {
        "x": "F"
    }

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
