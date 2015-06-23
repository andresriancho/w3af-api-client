REST API client for w3af
========================

Launch web application security scans using `w3af's REST API <http://docs.w3af.org/en/latest/api/index.html>`_

.. image:: https://circleci.com/gh/andresriancho/w3af-api-client.svg?style=svg
   :alt: Build Status
   :align: right
   :target: https://circleci.com/gh/andresriancho/w3af-api-client

Installation
============

::

    $ pip install --upgrade w3af-api-client


Usage
=====

The REST API client allows you to run scans and access results and log files.

::

    from w3af_api_client import Connection, Scan

    # Connect to the REST API
    conn = Connection('http://127.0.0.1:5000/')

    # Define the target and configuration
    scan_profile = file('/path/to/profile.pw3af').read()
    target_urls = ['http://example.target']

    scan = Scan(conn)
    scan.start(scan_profile, target_urls)

    # Wait some time for the scan to start and then
    print scan.get_log()
    print scan.get_findings()

Source code
===========

Developers love code, here's all you need to understand, use and extend the client:

* `w3af's REST API server <https://github.com/andresriancho/w3af/tree/master/w3af/core/ui/api/>`_
* `w3af's REST API client <https://github.com/andresriancho/w3af-api-client/>`_

Reporting bugs
==============

Report your issues and feature requests in `w3af-api-client's issue
tracker <https://github.com/andresriancho/w3af-api-client>`_ and we'll
be more than glad to fix them.

Pull requests are more than welcome!

