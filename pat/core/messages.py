#
# pat/core/messages.py
#
"""
Module acting as a forwarding agent of the messages protobuffer module. This
normalizes EnumTypeWrappers to enable easy attribute retreval using a
namedtuple. eg messages.TYPE.PUT instead of messages.TYPE.Value("PUT").
The original protobuffer is accessable by accesssing messages.pb. All other
(non-dunder) attributes are copied into this namespace.
"""


import sys
from collections import namedtuple
from google.protobuf.internal.enum_type_wrapper import EnumTypeWrapper
from . import messages_pb as pb

module = sys.modules[__name__]

# forward all EnumTypeWrappers as namedtuples
for key in dir(pb):
    item = getattr(pb, key)
    if isinstance(item, EnumTypeWrapper):
        name = item.DESCRIPTOR.full_name
        tup_type = namedtuple(name, item.keys())
        setattr(module, key, tup_type(**dict(item.items())))
    elif not key.startswith('__'):
        setattr(module, key, item)
