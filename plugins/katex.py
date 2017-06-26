from pelican import signals

def add_reader(readers):
    print readers.reader_classes

# This is how pelican works.
def register():
    signals.readers_init.connect(add_reader)
