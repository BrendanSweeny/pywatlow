Watlow Messaging Structure
==========================

Read Requests and Responses

+-----+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|55 ff|06|00|10|00|0a|76|02|03|01|06|01|01|0f|01|00|44|
+-----+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

======== ====
Preamble Type
======== ====
55FF     05
55FF     05
======== ====

Example Read Requests
---------------------

Where the response is a float:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Messages from CSV
  :file: messages_read_float.csv
  :header-rows: 1

Where the response is an integer:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Messages from CSV
  :file: messages_read_int.csv
  :header-rows: 1

Example Set Requests
--------------------

Where the value/response is a float:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. csv-table:: Messages from CSV
  :file: messages_set_float.csv
  :header-rows: 1
