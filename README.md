# EZ File Lock
> A simple cross-platform File Lock

## Quick start:
```shell
pip install ezfilelock
```
## Usage

### Use just like builtin method open()
```python
from ezfilelock import open

with open('xxx.txt','r') as f:
    print(f.read())
```

### Use FileLock instance
```python
from ezfilelock import FileLock
from builtin import open

with FileLock('xxx.txt'):
    # do continuous things with lock
    with open('xxx.txt','w') as f:
        f.write('hello')
    with open('xxx.txt','a') as f:
        f.write('world!')
    with open('xxx.txt','r') as f:
        f.read()
```

### Read Write Lock

> Cannot Write when Reading.
>
> Cannot Read when Writing.
>
> Can Read by multiple threads at the same time

```python
from ezfilelock import rwopen

with rwopen('xxx.txt',mode='w') as f:
    f.write('hello world')

with rwopen('xxx.txt',mode='r') as f:
    print(f.read())
```