==========================
把Android设备变成USB摄像头
==========================

:date: 2015-10-07
:slug: turn-android-into-usb-webcam


闲置的山寨Android设备也不能浪费啊。看上去只要装个\ `IP WebCam`__\ 就好了。实际上却比这折腾的多了。


.. __: https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en

.. more


首先，有些奇怪的设备在刚插入时，没法直接使用设备，会先进入给你的机器装驱动的模式，这样就没法用ADB了。需要用 usb_modeswitch 才行。

先用lsusb找到新插入USB设备的ID。

.. code::

    Bus 001 Device 001: ID 0001:0002 Vender Info

假如是像上面这样的，可以用以下命令。可能还需要 :code:`--huawei-mode` 之类的参数

.. code::

    usb_modeswitch -v 0001 -p 0002

ADB能连上之后，装上IP WebCam，设置好端口转发，就能用比如vlc，看摄像头的视频了。

参考\ `ipwebcam-gst`__\ 里的说明，检查是不是能用GStreamer播放。

.. __: https://github.com/bluezio/ipwebcam-gst/blob/master/prepare-videochat.sh


安装\ `v4l2loopback`__\ 内核模块。这样就能有 /dev/video0 了。可是有点小问题，在Fedora上并不能用GStreamer的v4l2sink把视频传进去，需要修改一下代码。

.. __: https://github.com/umlaeute/v4l2loopback


注意，Skype需要一些特别的参数，参考v4l2loopback \ `Wiki`__\ 里的说明

.. __: https://github.com/umlaeute/v4l2loopback/wiki/Skype
