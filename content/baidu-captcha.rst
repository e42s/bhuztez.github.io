=================================
用Tesseract识别百度空间留言验证码
=================================

:date: 2009-12-23
:modified: 2017-06-29
:slug: breaking-baidu-hi-captcha-with-tesseract
:tags: Tesseract, Baidu

本文写于很多年前，现在百度空间已经关闭了，所以发出来也无妨。主要是为了说明现有的工具都很强大了，不要想当然的以为画几个字符上去就可以当验证码了。现在的Tesseract相比当时有很多改进，里面提到的很多步骤都已经没必要了。

.. more

tombkeeper在\ `用gocr对付简单验证码`__\ 中指出简单的验证码用现有的OCR工具就可以识别出来了。借助更强大的\ Tesseract_\ ，不需要了解识别验证码相关的专门知识，也可以很容易的识别更复杂一些的验证码。这里就以百度空间留言验证码为例。

百度空间留言验证码用到了不少字体：Arial, Bookman Old Style, Century SchoolBook, Comic Sans MS, Courier New, Georgia, Palatino Linotype, Rockwell, Times New Roman, TrebuchetMS，还有一种没认出来的Script字体，不过仅出现在数字上，且出现次数也很少，这里就忽略了。特别注意出现过的字符只有123567ACEHKMNRTUWXY，Tesseract训练需要的图片里应该只包含这些字符。

百度空间留言验证码图片是JPEG格式的灰度图片，可能是因为JPEG编码引起的，放大之后可以看到白色的背景并不是纯白色的，而是有一些斑点。而Tesseract对这些噪音比较敏感，所以先把这些斑点去掉。就用非常简单的规则，和通常的编码相反，这里以白色为0，黑色为255，若一个点及其周围八个点的颜色值总和小于256就将它改成白色。另外有一些毫无疑问该识别对的，还是错了，试着用\ `Voronoi diagram`__\ 切开后分别识别再把结果合并到一起就对了。方便起见，这里就用\ Pymorph_\ 了。

最终，取了1000张验证码图片，其中663张能识别对。考虑到就没写几行代码，这结果也不赖了吧。

.. __: http://tombkeeper.blog.techweb.com.cn/archives/255
.. _Tesseract: https://code.google.com/p/tesseract-ocr/
.. __: https://en.wikipedia.org/wiki/Voronoi_diagram
.. _Pymorph: http://luispedro.org/software/pymorph/
