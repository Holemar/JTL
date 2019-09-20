# JTL
[English version](./README.md)  
JSON Transformation Language, JTL, 是一个像 `sed` 和 `awk` 的 JSON 解析器。
是一个简单的 json 转换语言，容易得像如下语句：

    > cat tests/faa1.json
    {
        ...
        "city": "Washington",
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

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.spring $ default \"one\" ", "y": "weather.temp $ default city "}'
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
将输入值转成字符串。日期则按日期格式转换。

### Bool

* `not`: 反转布尔值。
* `and`: 所有值都是 真 时返回 `true`, 否则返回 `false`.
* `or`: 其中一个值是 真 时返回 `true`, 所有值都是 假 时返回 `false`.

### Dictionary

#### `keys`
返回字典的 keys 列表。

#### `values`
返回字典的 values 列表。

#### `enumChange`
返回枚举dict对应的值。  
使用格式： `<SELECTOR> $ enumChange '{"F": "女", "M": "男"}'`  

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
使用格式： `<SELECTOR> $ enumFileChange 文件路径`  
文件路径可以使用绝对地址，也可以是相对于项目启动目录的路径。

如:

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
JTL支持各种加密hash函数: `md5`, `sha1`, `sha224`, `sha256`, `sha384`, `sha512`。另外，每种hash函数都支持 [HMAC's](https://en.wikipedia.org/wiki/Hash-based_message_authentication_code)。

### Math

* 基础(Basics): `abs`, `ceil`, `floor`
* 指数(Exponentials): `exp`, `lg`, `ln`, `log`, `sqrt`
* Flags: `isFinite`, `isNan`
* 三角(Trigonometry): `sin`, `cos`, `tan`
* 双曲三角学(Hyperbolic trigonometry): `sinh`, `cosh`, `tanh`
* 高级(Advanced): `erf`

### Sequence

#### `索引值`
返回列表里面指定索引位置的值，当索引下标越界时返回 `null`。 下标从 0 开始。

如:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "weather.temp $ words $ 1"}'
    {
        "x": "F"
    }

#### `count <ELEMENT>`
返回列表的元素数量。

#### `first`
返回列表的第一个元素。如果是空列表，则返回 `null`。

#### `last`
返回列表的最后一个元素。如果是空列表，则返回 `null`。

#### `rmFirst`
去掉列表的第一个元素，然后返回结果列表。

#### `rmLast`
去掉列表的最后一个元素，然后返回结果列表。

#### `rmNull`
去掉列表的所有`null`元素，然后返回结果列表。

#### `list`
将所有参数值作为列表返回，但去掉 `<SELECTOR>` 元素。
如:

    > cat tests/faa1.json | ./JTL/__init__.py '{"x": "* $ list weather.temp 1 \"ab\" city" }'
    {
        "x": ["66.0 F (18.9 C)", 1, "ab", "Washington"]
    }

##### 获取多个字段值，且以list形式返回

```python
from JTL import Interpreter

data = {
    "skill_type": "英语",
    "compet_level": "四级",
    "time_use": "三年外贸经验"
}
result = Interpreter.transform(data, '* $ list skill_type compet_level time_use ')
print(result)  # ['英语', '四级', '三年外贸经验']
```


##### 合并多个字段值

```python
from JTL import Interpreter

data = {
    "skill_type": "英语",
    "compet_level": "四级",
    "time_use": "三年外贸经验"
}
result = Interpreter.transform(data, '* $ list skill_type compet_level time_use $ join "-" ')
print(result)  # 英语-四级-三年外贸经验
```


##### 在多个字段中，获取有值的任意一个，按字段列表的优先顺序取

```python
from JTL import Interpreter

data = {
    "INTENTION_PLACE": None,
    "INTENTION_PLACE_ONE": "广东",
    "INTENTION_PLACE_TWO": "上海"
}
result = Interpreter.transform(data, '* $ list INTENTION_PLACE, INTENTION_PLACE_ONE, INTENTION_PLACE_TWO $ rmNull $ first')
print(result)  # 广东
```

#### `length`
返回列表的长度。

#### `max`
找出列表里的最大值。

#### `min`
找出列表里的最小值。

#### `sorted`
返回排序后的列表。

#### `sum`
取得列表里所有值的和。

#### `unique`
返回一个去除重复值之后的列表。

### String

* Case transformation: `capitalize`, `lower`, `swapCase`, `upper`
* Search: `find`, `replace`, `startsWith`, `endsWith`
* Split / join: `join`, `split`, `lines`, `unlines`, `words`, `unwords`
* Whitespace: `lstrip`, `rstrip`, `strip`


### 日期/时间

#### 日期/时间转成字符串 `toString`
将 `datetime.datetime`, `time` 类型按 `%Y-%m-%dT%H:%M:%S` 格式转成字符串。  
将 `datetime.date` 类型按 `%Y-%m-%d` 格式转成字符串。  
将 `datetime.time` 类型按 `%H:%M:%S` 格式转成字符串。  
用法: `<SELECTOR> $ toString`

#### 日期转成字符串 `dateToString`
将所有日期/时间类型默认按 `%Y-%m-%d` 格式转成字符串。  
第一个参数可以指定字符串格式，第二个参数(true/false)指定是否当日期/时间为`null`时取当前时间。  
用法: `<SELECTOR> $ dateToString "<format_str>"? default_now?`

#### 时间转成字符串 `datetimeToString`
将所有日期/时间类型默认按 `%Y-%m-%dT%H:%M:%S` 格式转成字符串。  
第一个参数可以指定字符串格式，第二个参数(true/false)指定是否当日期/时间为`null`时取当前时间。  
用法: `<SELECTOR> $ datetimeToString "<format_str>"? default_now?`

#### 转成日期 `toDate`
将所有日期/时间类型转成`datetime.date`类型。  
第一个参数(true/false)指定是否当日期/时间为`null`时取当前时间。第二个参数当选择器的选择结果是字符串时，可以指定来源字符串的格式。  
用法: `<SELECTOR> $ toDate default_now? "<from_format_str>"? `

#### 转成时间 `toDatetime`
将所有日期/时间类型转成`datetime.datetime`类型。  
第一个参数(true/false)指定是否当日期/时间为`null`时取当前时间。第二个参数当选择器的选择结果是字符串时，可以指定来源字符串的格式。  
用法: `<SELECTOR> $ toDatetime default_now? "<from_format_str>"? `
