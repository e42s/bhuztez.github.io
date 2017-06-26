======================
Python模拟HTML表单提交
======================

:date: 2016-06-30
:slug: multipart-form-data-in-python
:tags: Python, HTTP

HTML表单里有一种类型是 :code:`multipart/form-data` ，

搜了一下结果发现要么是远古时期的，要么推荐用requests，就是没有人推荐用标准库的方法。Python明明自带MIME库了，用标准库就足够了嘛。

.. more

.. code:: python

    from urllib2 import Request
    from email.message import Message


    class Form(Message):

        def __init__(self):
            Message.__init__(self)
            self.add_header('Content-Type', 'multipart/form-data')
            self._payload = []

        def _write_headers(self, _generator):
            # DARK MAGIC followed
            pass


    class Field(Message):

        def __init__(self,name,text):
            Message.__init__(self)
            self.add_header('Content-Disposition','form-data',name=name)
            self.set_payload(text,None)


    def make_request(url,form_data):
        form = Form()

        for name,value in form_data.iteritems():
            form.attach(Field(name,str(value)))

        data = form.as_string()
        # THIS IS A SEPARATION BARRIER
        # NEVER LET CODE MOVE ACROSS THIS
        headers = {'Content-Type': form['Content-Type']}

        return Request(url,data,headers)
