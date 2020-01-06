# pip/pip3升级后提示Cannot import name main的解决办法

- 使用文本编辑器打开`/usr/bin/pip`或`/usr/bin/pip3`，进行如下修改：

    1. 将`from pip import main`改为`from pip import __main__`

    1. 将`sys.exit(main())`改为`sys.exit(__main__._main())`

- 之后，执行命令验证

```bash
# pip (Python 2)
pip -V
# pip3 (Python 3)
pip3 -V
```

- 例如，修改前

```python
import re
import sys
from pip import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

- 修改后

```python
import re
import sys
from pip import __main__

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(__main__._main())
```