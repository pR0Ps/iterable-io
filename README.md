iterable-io
===========
[![Status](https://github.com/pR0Ps/iterable-io/workflows/tests/badge.svg)](https://github.com/pR0Ps/iterable-io/actions/workflows/tests.yml)
[![Version](https://img.shields.io/pypi/v/iterable-io.svg)](https://pypi.org/project/iterable-io/)
![Python](https://img.shields.io/pypi/pyversions/iterable-io.svg)

`iterable-io` is a small Python library that provides an adapter so that it's possible to read from
[iterable](https://docs.python.org/3/glossary.html#term-iterable) objects in the same way as
[file-like](https://docs.python.org/3/glossary.html#term-file-object) objects.

It is primarily useful as "glue" between two incompatible interfaces. As an example, in the case
where one interface expects a file-like object to call `.read()` on, and the other only provides a
generator of bytes.

One way to solve this issue would be to write all the bytes in the generator to a temporary file,
then provide that file instead, but if the generator produces a large amount of data then this is
both slow to start, and resource-intensive.

This library allows streaming data between these two incompatible interfaces so as data is requested
by `.read()`, it's pulled from the iterable. This keeps resource usage low and removes the startup
delay.


Installation
------------
```
pip install iterable-io
```


Documentation
-------------
The functionality of this library is accessed via a single function: `open_iterable()`.

`open_iterable()` is designed to work the same was as the builtin `open()`, except that it takes an
iterable to "open" instead of a file. For example, it can open the iterable in binary or text mode,
has options for buffering, encoding, etc. See the docstring of `open_iterable` for more detailed
documentation.


Simple examples
---------------
The following examples should be enough to understand in which cases `open_iterable()` would be
useful and get a high-level understanding of how to use it:

Read bytes from a generator of bytes:
```python
gen = generate_bytes()

# adapt the generator to a file-like object in binary mode
# (fp.read() will return bytes)
fp = open_iterable(gen, "rb")

while chunk := fp.read(4096):
    process_chunk(chunk)
```

Read lines of text from a generator of bytes:
```python
gen = generate_bytes()

# adapt the generator to a file-like object in text mode
# (fp.read() will return a string, fp.readline is also available)
fp = open_iterable(gen, "rt", encoding="utf-8")

for line in fp:
    process_line_of_text(line)
```


Tests
-----
This package contains extensive tests. To run them, install `pytest` (`pip install pytest`) and run
`py.test` in the project directory.


License
-------
Licensed under the [GNU LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html).
