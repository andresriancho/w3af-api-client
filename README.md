REST API client for w3af | Python 3
========================

Launch web application security scans using [w3af's REST API](http://docs.w3af.org/en/latest/api/index.html)

# Update for Python 3

This is a forked and updated version of w3af REST API client for Python 3.

Original project  : https://github.com/andresriancho/w3af-api-client


# Installation

```bash=
    $ pip install --upgrade w3af-api-client
```


# Usage

The REST API client allows you to run scans and access results and log files.

```bash=
    from w3af_api_client import Connection, Scan
    
    # Connect to the REST API and get it's version
    conn = Connection('http://127.0.0.1:5000/')
    print conn.get_version()
    
    # Define the target and configuration
    scan_profile = file('/path/to/profile.pw3af').read()
    target_urls = ['http://example.target']
    
    scan = Scan(conn)
    scan.start(scan_profile, target_urls)
    
    # Wait some time for the scan to start and then
    scan.get_urls()
    scan.get_log()
    scan.get_findings()
```

# Source code

Developers love code, here's all you need to understand, use and extend the client:

* `w3af's REST API server <https://github.com/andresriancho/w3af/tree/master/w3af/core/ui/api/>`_
* `w3af's REST API client <https://github.com/andresriancho/w3af-api-client/>`_

# Reporting bugs

Report your issues and feature requests in [w3af-api-client's issue tracker](https://github.com/andresriancho/w3af-api-client>) and we'll be more than glad to fix them.

Pull requests are more than welcome!
