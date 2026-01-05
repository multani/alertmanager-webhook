import json


def json_printer(payload: bytes) -> None:
    """Parse a JSON payload and prints it back in a consistent, compact way.

    >>> json_printer(b'{"foo": "bar", "aaa": "bbb"}')
    {"aaa": "bbb", "foo": "bar"}

    """

    obj = json.loads(payload)
    data = json.dumps(obj, indent=None, sort_keys=True, ensure_ascii=False)
    print(data)
