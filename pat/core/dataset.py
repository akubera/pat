#
# pat/core/dataset.py
#


class Dataset:

    def __init__(self, name, dat):
        self.name = name
        self.dat = dat

    def get(self, key):
        self.dat.get(key, dataset=self.name)

    def put(self, key, value):
        self.dat.put(key, value, dataset=self.name)

    def delete(self, key):
        self.dat.del_(key, dataset=self.name)

    def batch(self, batch):
        self.dat.batch(batch, dataset=self.name)

    def create_read_stream(self, **opts):
        opts.setdefault('dataset', self.name)
        return self.dat.create_read_stream(**opts)

    def create_write_stream(self, **opts):
        opts.setdefault('dataset', self.name)
        return self.dat.create_write_stream(**opts)

    def create_file_read_stream(self, **opts):
        opts.setdefault('dataset', self.name)
        return self.dat.create_file_read_stream(**opts)

    def create_file_write_stream(self, **opts):
        opts.setdefault('dataset', self.name)
        return self.dat.create_file_write_stream(**opts)
