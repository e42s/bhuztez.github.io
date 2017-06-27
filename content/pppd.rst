============
编写pppd插件
============

:date: 2008-11-06
:slug: pppd-plugin
:tags: PPP, How-to

pppd关于插件的说明，只有代码树最顶上那个\ :code:`PLUGINS`\ 文件。按里面的说法，先\ :code:`yum install ppp-devel`\ ，在C代码中加上\ :code:`#include <pppd/pppd.h>`\ 和\ :code:`char pppd_version[] = VERSION;`\ 以确保plugin能被pppd使用，就可以了。

.. more

然而，有些需要注意的地方在里面并没有提到，得看现成的插件代码才知道是怎么回事。比如\ :code:`pad_passwd_hook`\ ，是会被多次调用的，而且第一次调用时，\ :code:`passwd`\ 参数是个空指针。假如你的插件需要修改用户名，你还需要自行判断之前有没有修改过。以下是参考代码

.. code:: c

    static char pwd[MAXSECRETLEN] = {0};
    static int is_name_modified = 0;

    static option_t options[] = {
        { "pwd", o_string, pwd,
          "pwd",
          OPT_STATIC, NULL, MAXSECRETLEN-1 },
        { NULL }
    };

    static int
    get_credentials(char *user, char *passwd) {
        if (!is_name_modified) {
            modify(user);
            is_name_modified = 1;
        }

        if (passwd != NULL) {
            strcpy(passwd, pwd);
        }

        return 1;
    }

    void
    plugin_init(void) {
        add_options(options);
        pap_passwd_hook = get_credentials;
    }
