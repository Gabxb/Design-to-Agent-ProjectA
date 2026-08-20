# Python 语法速查

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Item:
    name: str

def normalize(value: str) -> str:
    if not value.strip():
        raise ValueError("value must not be empty")
    return value.strip()
```

重点：类型提示、明确输入输出、异常、测试和模块边界。
