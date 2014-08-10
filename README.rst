=============
zabbix-client
=============

**zabbix-client** is a Zabbix API wrapper written in Python. It works on
Python 2.6+ and 3.2+.

Zabbix API
----------

Zabbix API was introduced in Zabbix 1.8 and allows you to create, update
and fetch Zabbix objects (like hosts, items, graphs and others) through
the JSON-RPC 2.0 protocol.

Zabbix API documentation:

* `Getting started with Zabbix API`_
* `Zabbix API description`_
* `Zabbix API method reference`_

JSON-RPC documentation:

* `JSON-RPC 2.0 specification`_

**zabbix-client** supports all Zabbix versions including the JSON-RPC
API, starting with Zabbix 1.8.

Usage
-----

Calling a method that does not require authentication::

    >>> from zabbix_client import ZabbixServerProxy
    >>> s = ZabbixServerProxy('http://localhost/zabbix')
    >>> s.apiinfo.version()
    '2.0.12'

Calling a method that requires previous authentication::

    >>> from zabbix_client import ZabbixServerProxy
    >>> s = ZabbixServerProxy('http://localhost/zabbix')
    >>> s.user.login(user='Admin', password='zabbix')
    '44cfb35933e3e75ef51988845ab15e8b'
    >>> s.host.get(output=['hostid', 'host'])
    [{'host': 'Zabbix server', 'hostid': '10084'},
        {'host': 'Test', 'hostid': '10085'}]
    >>> s.user.logout()
    True

License
-------

Licensed under the Apache License.

.. _Getting started with Zabbix API: https://www.zabbix.com/documentation/1.8/api/getting_started
.. _Zabbix API description: https://www.zabbix.com/documentation/2.2/manual/api
.. _Zabbix API method reference: https://www.zabbix.com/documentation/2.2/manual/api/reference
.. _JSON-RPC 2.0 specification: http://www.jsonrpc.org/specification
