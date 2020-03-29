# pysonic

pysonic is a Python client for lightweight and fast search engine - Sonic

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install pysonic --upgrade
```

## Usage

```python
from pysonic import pysonic

c = pysonic.Client()
with c:
    resp = c.ping()
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
