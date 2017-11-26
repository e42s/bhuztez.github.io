==============
Heartbleed漏洞
==============

:date: 2014-04-13
:slug: heartbleed
:tags: OpenSSL
:status: draft

最近爆出的\ `Heartbleed`__\ 漏洞实际上宣告了互联网安全已经破产了很久了。不管怎么样，还是首先提醒一下，这次的漏洞后果非常非常严重，至少应该尽快更新所有用到受影响版本的OpenSSL软件。不仅仅是服务端程序受影响，客户端程序也同样受影响，而且很多软件都选择自行编译一份OpenSSL库，所以即便使用的操作系统不受影响，自行安装的程序只要需要联网就很可能受影响。你可以检查一下软件安装目录下的文件。Windows下有libeay32.dll、ssleay32.dll或者类似名字的文件，Mac OS X下有libssl.dynlib或者类似名字的文件，Linux下有libssl.so或者类似名字的文件，非常有可能是受影响的。假如发现了这些文件，而在4月8日以后软件开发商没有发布过修补这个漏洞的新版本，请务必要第一时间联系软件开发商及时更新软件。

.. __: http://heartbleed.com/

.. more

这次的问题是出现在对TLS协议的heartbeat的处理上，这也是漏洞会被命名为Heartbleed的原因。我觉得TLS协议上的Heartbeat的设计也很有问题。为什么Heartbeat的payload是可变长度且可长达64K，而不是固定的长度比如64个字节？假如可变的是padding的长度而不是payload的长度，这次的漏洞根本就不会出现。同时，OpenSSL对malloc的封装把问题变得更严重了，越界读到的内存基本都在OpenSSL之前申请的范围之内，也就是都算得上是敏感内容。我感觉这里的内存分配应该把不同数据内容不同连接隔离开啊，每一片内存前后放两个内存页用来在发生越界的时候直接crash掉程序。\ `Akamai最近向OpenSSL提交了一个补丁`__\ ，表明他们在几年前就已经应用了这样的想法，不过他们只把这种措施限制在ASN.1格式处理上了，也就是只保护了证书和私钥，其他数据还是混在一起的，\ `私钥还是有可能从中间结果泄露`__\ 。

.. __: http://article.gmane.org/gmane.comp.encryption.openssl.user/51243
.. __: https://blogs.akamai.com/2014/04/heartbleed-update-v3.html


要通过\ `静态分析`__\ 找出这个漏洞也不是不可能的。很不幸，Coverity没有发现问题，Frama-C是可以检查出问题，但是要让OpenSSL都能通过Frama-C检查也不是一件容易的事。很难想像，\ `NSA没在第一时间发现这个漏洞`__\ 。

.. __: http://blog.regehr.org/archives/1125
.. __: http://blogs.wsj.com/digits/2014/04/11/nsa-says-it-wasnt-previously-aware-of-heartbleed/

问题出在TLS协议层，基本上就不可能从日志上查出被攻击的迹象。所以，有X.509证书的赶紧去申请个新的。公共的Wifi就不要连了。特别提醒一点，由于这一次会导致海量证书被revoke，所以浏览器一定要强制OCSP，不然被中间人用偷来的私钥攻击了，你啥也不知道。
