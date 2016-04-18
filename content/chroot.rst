创建Fedora chroot
=================

:date: 2016-04-08
:slug: chroot


在Fedora 21之前，要创建chroot都比较容易，可以参考 `Five steps to create Fedora chroot jail using yum`__ 。

.. __: http://blog.parahard.com/2011/06/five-steps-to-create-fedora-chroot-jail.html

.. more


自从Fedora 21开始，fedora-release不再像以前那样了。fedora-release会依赖bash，bash又会依赖更多包，一个个去找过来是不现实的。所以只能强制安装了。

先建好目录，初始化RPM的db

.. code::

    mkdir -p /path/to/chroot/root
    rpm --root "/path/to/chroot/root" --initdb

装包时，需要让rpm相信自己是root。比如可以用 :code:`userns spawn -n chroot --user -- /bin/bash` 来建一个user namespace，因为安装需要联网，所以不建新的network namespace。更新的Fedora已经用dnf替换yum了，所以更推荐使用dnf来安装。

.. code::

    rpm -ivh --nodeps --root "/path/to/chroot/root" fedora-repos-23-1.noarch.rpm fedora-release-23-1.noarch.rpm
    dnf --installroot="/path/to/chroot/root" install coreutils bash

安装完成后，就可以进入chroot了

.. code::

    chroot "/path/to/chroot/root" /bin/bash
