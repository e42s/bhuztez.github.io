ArchLinux从AUR安装octave-forge遇到gcc-fortran conflicts with gcc-libs
=====================================================================

:date: 2010-01-02
:slug: install-octave-forge-from-aur


从\ `这里`__\ 看，应该2009年8月31日才加上的。其实 :code:`gcc-fortran` 是不一定要的，把 :code:`makedepends` 那行去掉就好了，囧

__ http://aur.archlinux.org/packages.php?ID=20824
