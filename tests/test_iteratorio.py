#!/usr/bin/env python

import io

from iterableio import RawIterableReader, open_iterable

import pytest


@pytest.mark.parametrize("mode, buffering, encoding, errors, newline",[
    # bad modes
    ("", -1, None, None, None),
    ("abc", -1, None, None, None),
    ("rtb", -1, None, None, None),
    ("rt", 0, None, None, None),  # need buffering
    ("rt", "bad int", None, None, None),  # invalid buffering int
    # can't provide text decoding params in binary mode
    ("rb", 0, "utf-8", None, None),
    ("rb", 0, None, "ignore", None),
    ("rb", 0, None, None, "\n"),
])
def test_invalid_input(mode, buffering, encoding, errors, newline):
    """Test that invalid params are caught"""
    with pytest.raises((ValueError, TypeError, LookupError)):
        open_iterable([], mode, buffering, encoding, errors, newline)


@pytest.mark.parametrize("buffering", (0, -1, 1))
def test_reading(buffering):

    def gen():
        yield from (
            b'\x01\x02\x03\x04\x05',
            b"abcde",
            b"fghij",
            b"klmno",
            b"qrstu",
            b"vwxyz",
            b'\x06\x07\x08\x09\x10',
        )

    _data = b"".join(gen())

    with open_iterable(gen(), "rb", buffering=buffering) as i:
        assert i.readable()
        assert not i.seekable()
        assert not i.writable()

        cnt = 0
        for amt in (0, 1, 2, 3, 4, 5, 10, 1, 1, 0):
            d = i.read(amt)
            assert len(d) == amt
            assert d == _data[cnt:cnt+amt]
            cnt += amt
            assert i.tell() == cnt

        assert i.read() == _data[cnt:]
        assert i.read() == b""

        assert i.tell() == len(_data)


def test_returned_class():
    """Test that the correct class is returned depending on the mode and buffering spec"""
    assert isinstance(open_iterable([], "rb", buffering=0), RawIterableReader)
    assert isinstance(open_iterable([], "rb", buffering=-1), io.BufferedReader)
    assert isinstance(open_iterable([], "rb", buffering=1), io.BufferedReader)
    assert isinstance(open_iterable([], "rt", buffering=-1), io.TextIOWrapper)
    assert isinstance(open_iterable([], "rt", buffering=1), io.TextIOWrapper)


@pytest.mark.parametrize("mode, buffering",[
    ("rb", 0),
    ("rb", -1),
    ("rt", -1),
])
def test_contextmgr_close(mode, buffering):
    with open_iterable([], mode, buffering) as i:
        assert not i.closed
    assert i.closed


@pytest.mark.parametrize("mode, buffering",[
    ("rb", 0),
    ("rb", -1),
    ("rt", -1),
])
def test_unreadable_after_close(mode, buffering):

    i = open_iterable([b"12345"], mode, buffering)
    assert not i.read(0)
    assert i.read(1) in (b"1", "1")
    assert not i.closed

    i.close()
    assert i.closed

    with pytest.raises(ValueError, match="closed"):
        i.read()
    with pytest.raises(ValueError, match="closed"):
        i.tell()


def test_yield_empty_bytes():
    """Test that a generator is only 'done' when it stops yielding, not when it yields empty bytes"""
    def gen():
        yield from (
            b"1",
            b"", b"", b"", b"", b"", b"", b"",
            b"2", b"3",
            b"", b"", b"", b"", b"", b"",
            b"4",
        )

    i = RawIterableReader(gen())
    out = []
    while True:
        b = i.read(1)
        if not b:
            break
        out.append(b)

    assert len(out) == 4
    assert b"".join(out) == b"1234"


def test_read_text():
    def gen():
        # 9 lines yielded in non-line chunks
        yield from (
            x.encode("utf-8") for x in (
                "this is a line\n",
                "",
                "",
                "_a",
                "another line\n",
                "another line1\n",
                "another line2\n",
                "another line_",
                "a",
                "aaaaaaa\nbbbbbbbb",
                "_",
                "1",
                "2",
                "3",
                "4",
                "5",
                "_line line line another line actually\n",
                "another line\n",
                "ending line\n",
                "actual ending line no trailing newline",
            )
        )

    real = "".join(x.decode("utf-8") for x in gen())

    # read across chunks and lines
    with open_iterable(gen(), encoding="utf-8") as i:
        assert i.read(10) == real[:10]
        assert i.read(10) == real[10:20]

    with open_iterable(gen(), encoding="utf-8") as i:
        lines = list(i)

    with open_iterable(gen(), encoding="utf-8") as i:
        assert lines == i.readlines()


    assert len(lines) == len(real.splitlines()) == 9
    assert "".join(lines) ==  real
