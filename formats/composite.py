from formats.format import Format

class Composite(Format):
    
    def __init__(self, schema_in, schema_out):
        Format.__init__(self, schema_in, schema_out)

        self.setup()

    def setup(self):
        raise NotImplementedError()
