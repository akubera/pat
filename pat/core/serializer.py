#
# pat/core/serializer.py
#

import json


def json_encode(obj):
    return json.dumps(obj).encode()


def json_decode(obj):
    return json.loads(obj.decode())


def utf8_encode(obj):
    return json_encode(obj)


def utf8_decode(obj):
    return json_decode(obj)


def binary_encode(obj):
    return obj.encode()


def binary_decode(obj):
    return obj.encode()


class Serializer:

    encode_dict = {
        'json': json_encode,
        'utf8': utf8_encode,
        'bin': binary_encode,
    }

    decode_dict = {
        'json': json_decode,
        'utf8': utf8_decode,
        'bin': binary_decode,
    }

    @classmethod
    def encode(cls, method, obj):
        return cls.encode_dict[method](obj)

    @classmethod
    def decode(cls, method, obj):
        return cls.decode_dict[method](obj)
