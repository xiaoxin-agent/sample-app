"""示例：一个简单的计算器模块，pipeline 用它演示构建 / 测试 / 打包。"""


def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为 0")
    return a / b
