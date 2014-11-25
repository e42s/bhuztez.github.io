pppd插件编写
============

:date: 2008-11-06
:slug: pppd-plugin

先 :code:`yum install ppp-devel` ，接着就可以在代码中使用 :code:`#include <pppd/pppd.h>` 和 :code:`char pppd_version[] = VERSION;` 以确保plugin能被pppd使用。

pap_passwd_hook被调用的过程还是很令人困惑的。首先，第一次被调用的时候，参数user是有分配空间的，为了让pap_passwd_hook被调用，是不能传入password的，导致第一次被调用的时候，参数passwd没有被分配空间，是NULL。若第一次修改了用户名，第二次调用的时候会传入修改过的用户名，而第二次passwd被分配了空间，此时可以strcpy。

.. more

所以还得这么干：

.. code:: c

    static char pwd[MAXSECRETLEN] = {0};
    static int is_name_modified = 0;

    static option_t options[] = {
        { "pwd", o_string, pwd,
          "pwd",
          OPT_STATIC, NULL, MAXSECRETLEN-1 },
        { NULL }
    };

    static int pap_passwd_hooker(char *user, char* passwd) {
        // Note: Do not modify the username twice in a session.
        if (!is_name_modified) {
            modify(user);
            is_name_modified = 1;
        }

        // Note: passwd == NULL the first time this function is called
        if (passwd != NULL) {
            strcpy(passwd, pwd);
        }

        return 1;
    }

    void plugin_init(void) {
        add_options(options);
        pap_passwd_hook = pap_passwd_hooker;
    }
