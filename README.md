# 随机执行方法的有限状态机

用以执行某些测试任务

## 使用方法

```python
from rsm import RSM

class Test(RSM):
    state_info = {
                    'entry':{'t1':0.5,'t2':0.5},
                    't1':{'complete':0.1,'t2':0.9},
                    't2':{'complete':0.1, 't1':0.9}
                    }

    def t1(self):
        print(1)

    def t2(self):
        print(2)


if __name__ == '__main__':
    t = Test()
    t.run()
```

- 将状态的信息写入state_info的类变量中， 每项的含义表示执行到特定的方法后，进入下一个方法的概率表。这实际上表示了一个概率转换矩阵 
- 参与状态的方法在执行时不包含任何参数，可以使用实例变量进行变量传递。
