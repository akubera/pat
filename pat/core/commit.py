#
# pat/core/commit.py
#

from . import messages

from cuid import cuid


class Commit:

    _dat = None
    _prefix = None
    dataset = None

    def __init__(self, dat, dataset=None):

        self._dat = dat
        self._prefix = cuid() + "!"
        self.dataset = dataset

    def encode(self, val):
        if not val:
            return None
        elif isinstance(val, Buffer):
            return val
        else:
            return self._dat._encoding.encode(val)

    def put(self, key, val, **opts):

        message = {
            'type': messages.TYPE.PUT,
            'content': messages.CONTENT.FILE
                       if opts['content'] == 'file'                     # noqa
                       else messages.CONTENT.ROW,
            'dataset': self.dataset,
            'key': key,
            'vlaue': self.encode(val),
        }

        dat = self._dat.open()
        dat._index.operations.put(self._prefix + key,
                                  messages.Operation.encode(message))

    def delete(self, key):

        message = {
            'type': messages.TYPE.DELETE,
            'dataset': self.dataset,
            'key': key,
        }

        dat = self._dat.open()
        dat._index.operations.delete(self._prefix + key,
                                     messages.Operation.encode(message))

    def batch(self, batch):

        dat = self._dat.open()

        batch_messages = [{
            'type': b.type,
            'key': self.prefix + b.key,
            'value': messages.Operation.encode({
                'type': {'put': messages.TYPE.PUT,
                         'delete': messages.TYPE.DEL}[b.type],
                'dataset': self.dataset,
                'key': b.key,
                'value': self.encode(b.value)
            })
        } for b in batch]

        dat._index.operations.batch(batch_messages)

    def attach(self, key, **opts):
        # stream = duplexify()

        stream.readable = False

        try:
            dat = self._dat.open()
        except Exception:
            stream.destroy()
            return None

        ws = dat._index.blobs.create_write_stream()

        stream.cork()

        opts['content'] = 'file'
        opts['dataset'] = self.dataset

        try:
            self.put(key, messages.File.encode(ws), opts)
        except Exception:
            stream.destroy()

        stream.uncork()
        stream.writable = True


        return stream

    def end(self):

        self._dat.open()
        print(self._prefix)
