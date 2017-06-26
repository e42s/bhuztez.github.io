from pelican import signals

def content_object_init(instance):
    content = instance._content
    if content is not None:
        instance._summary = content[:content.find("<!-- more -->")]

def register():
    signals.content_object_init.connect(content_object_init)
