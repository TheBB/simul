from formats.format import Format

class Composite(Format):
    
    def __init__(self, schema_in, schema_out):
        Format.__init__(self, schema_in, schema_out)

        self.setup()

    def is_fixed(self):
        raise NotImplementedError()

    def is_modified(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def should_use_mc(self):
        raise NotImplementedError()

    def fill(self):
        raise NotImplementedError()

    def instances(self):
        raise NotImplementedError()

    def random_instance(self, new=False):
        raise NotImplementedError()

    def compute_mc(self, runs=1000):
        raise NotImplementedError()

    def compute_exact(self):
        raise NotImplementedError()

    def detail(self, strings):
        raise NotImplementedError()

    def summary(self, strings, title=None):
        raise NotImplementedError()

    def setup(self):
        raise NotImplementedError()

    def get_match(self, key):
        raise NotImplementedError()
