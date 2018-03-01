
follow-up post to  2018-03-02 logstash part2


https://github.com/logstash-plugins/logstash-input-journald



Store syslog too
================

.. todo:: syslog pattern


In *Ubuntu 16.04*, it is the file ``/etc/rsyslog.conf``:

.. code-block:: text
   :linenos:
   :emphasize-lines: 0

   # provides TCP syslog reception
   module(load="imtcp")
   input(type="imtcp" port="514")

Restart the service with ``systemctl restart rsyslog.service``.

Check that the service is listening on port 514:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ netstat -tulpn | grep 514
   tcp    0   0 0.0.0.0:514      0.0.0.0:*      LISTEN    2196/rsyslogd
   tcp6   0   0 :::514           :::*           LISTEN    2196/rsyslogd

You're good to go when you see this.


