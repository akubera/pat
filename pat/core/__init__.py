#
# pat/core/__init__.py
#

import sys

from . import messages

#
# module = sys.modules[__name__]
# print(module)
#
# from .messages import (
#     TYPE,
#     CONTENT,
#     COMMIT_TYPE,
# )
#
# print(dir(TYPE), COMMIT_TYPE.items())
#
# (_, PUT), (_, DELETE) = TYPE.items()
#
# (_, ROW), (_, FILE) = CONTENT.items()
# #
# # (_, DATA), \
# # (_, TRANSACTION_DATA), \
# # (_, TRANSACTION_START), \
# # (_, TRANSACTION_END) = COMMIT_TYPE.items()
#
# for k, v in COMMIT_TYPE.items():
#     module.__setattr__(k, v)
#
#
# del _
