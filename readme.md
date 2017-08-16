# Bittrex RESTful API - Python 3 module

API wrapper for Bittrex API v1.1. Full API documentation available here:

https://bittrex.com/home/api

## Basic use
Import class from module:
```python
from bittrex import Bittrex
```
Create instance:
```python
bittrex = Bittrex('<api-key>', '<api-secret>')
```

## Methods' names
Methods name convention is based on API documentation with underscore dividing each word. Example:
```
getmarketsummary?market=btc-ltc --> bittrex.get_market_summary('btc-ltc')
```

