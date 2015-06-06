Prestans 2.0
============

A WSGI compliant REST micro-framework.

.. image:: https://pypip.in/version/prestans/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/prestans/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/prestans/badge/?version=latest
        :target: https://prestans.readthedocs.org/
        :alt: Documentation Status

Prestans is a REST micro-framework built right on top of WSGI, designed to perform and co-exists with other middleware and frameworks that you employ. Our target audience are developers building large REST backends for use with pure Ajax (using a framework like Google Closure) or mobile applications. prestans is designed for you to "take as much or as little" as you like.

We recommend you install via `pip <https://pypi.python.org/pypi/prestans/>`_.

Features:

- Built right on top of WSGI, designed ground up to cooperate with other frameworks
- Strong representative of REST philosophies leveraging HTTP headers and verbs
- Support for multiple dialects, including formalised patterns for binary content 
- Handlers maps HTTP verbs to implemented class methods, complimented  with custom request parser and response writer (built on top of WebOb)
- Unforgivingly strict parsing of requests and responses to ensure data integrity
- Helper methods to ease transformation of persistent objects to REST responses
- Pluggable integration to authentication

Prestans ensures that we provide extensive and useful documentation, published at available on `Read The Docs <http://docs.prestans.org>`_. Sphinx source available on `Github <http://github.com/prestans/prestans-docs/>`_.

Prestans also offers a set of `client side tools <https://github.com/prestans/prestans-client/>`_ to compliment Google Closure.

If you are still wondering prestans is a latin word meaning "excellent, distinguished, imminent."

Getting Help
^^^^^^^^^^^^

We recommend the use of our mailing lists as the primary way of getting help:

- `Discuss <http://groups.google.com/group/prestans-discuss>`_ used for general discussion.
- `Announce <http://groups.google.com/group/prestans-announce>`_ used for release and security announcements

Reporting Issues
^^^^^^^^^^^^^^^^

We prefer the use of our `Issue Tracker on Github <https://github.com/anomaly/prestans/issues>`_, to triage feature requests, bug reports.

Before you lodge a lodge a ticket:

- Seek wisdom from our comprehensive `documentation <https://prestans.readthedocs.org>`_
- Check to ensure that you are not lodging a duplicate request
- Search the Web to see that it’s not something to do with your server environment (versions of Web server, WSGI connectors, etc)
- Ensure that you ask a question on our list, there might already be answer out there or we might have already acknowledged the issue

When reporting issues:

- Include as much detail as you can about your environment (e.g Server OS, Web Server Version, WSGI connector)
- Steps that we can use to replicate the bug
- Share a bit of your application code with us, it goes a long way to replicate issues
