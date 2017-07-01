=======================
通过浏览器签发X.509证书
=======================

:date: 2011-04-03
:modified: 2017-07-01
:slug: certificate-request-from-browser
:tags: X.509

本文写于很多年前。因为\ :code:`<keygen>`\ 已经淘汰了\ [#]_\ ，所以已经完全没有意义了。同时，StartCom被收购之后，各大浏览器默认都不信任了，而pyOpenSSL也被cryptography取代了。

.. [#] https://developer.mozilla.org/en-US/docs/Web/HTML/Element/keygen

.. more

StartCom的免费证书是直接通过浏览器签发的。而通常X.509证书请求，都是要自己用OpenSSL生成的。看了一下在浏览器这边就是用了\ :code:`<keygen>`\ 。这个在Django里可以这么写。

.. code:: python

    from django import forms
    from django.utils.safestring import mark_safe
    from django.forms.util import flatatt

    import re
    from OpenSSL import crypto


    class KeygenWidget(forms.Widget):
        def render(self, name, value, attrs=None):
            if value is None: value = ''
            final_attrs = self.build_attrs(attrs, name=name)
            return mark_safe(u'<keygen%s />' % flatatt(final_attrs))


    class KeygenField(forms.CharField):
        widget = KeygenWidget

        def to_python(self, value):
            try:
                spki = crypto.NetscapeSPKI(re.sub(r'\s', '', value))
                if spki.verify(spki.get_pubkey()):
                    return spki
            except crypto.Error:
                pass
            raise forms.ValidationError("invalid key")


而返回的时候要用一个\ :code:`multipart/mixed`\ 的Response，证书导出成ASN1格式后，对应的部分Content-Type应该设置成\ :code:`application/x-x509-user-cert`\ 。只要CA证书在之前已经导入浏览器(Firefox)了，得到这个返回之后，浏览器会自动把CA证书，私钥，和返回的证书关联起来，从证书管理界面能直接导出p12文件。
