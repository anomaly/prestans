prestans, a WSGI compliant REST micro-framework
===============================================

prestans is a REST micro-framework built right on top of WSGI, designed perform and fit right in with any other WSGI middleware and frameworks you might already employ. It's mainly aimed towards developers building serious REST backends for use with pure Ajax (using a framework like Google Closure) or mobile applications. prestans is designed for you to "take as much or as little" you like, although we do think that it all works really well together.

Key features:

* Inbuilt URL handler so you use prestans directly on top of WSGI
* Wel defined handler lifecycle, mapped to HTTP verbs with pre and post execution hooks
* Strong reusable validation rules for incoming and outoging data payloads
* Easy integration (e.g Authentication, Caching, Throttling ) with existing WSGI framework and middleware by introducing a pattern of providers
* Support for multiple serialization methods
* Completely extendable by allowing you to write your own Providers
* Designed for applications with pure Ajax (e.g Gmail) or native mobile clients
* Extensive and useful documentation, published on [Github](http://github.com/prestans/prestans-docs, "Docs source") and available on [Read The Docs](http://docs.prestans.org "prestans documentation")

And incase you are still wondering prestans is a latin word meaning "excellent, distinguished, imminent."

Getting Help
------------

We recommend the use of our mailing lists as the primary way of getting help

* [Discuss](http://groups.google.com/group/prestans-discuss, "Discuss") used for general discussion.
* [Announce](http://groups.google.com/group/prestans-announce, "Announce") used for release and security announcements


Reporting Issues
----------------

We prefer the use of our [Issue Tracker on Github](https://github.com/prestans/prestans/issues, "Issue Tracker"), to triage feature requests, bug reports.

Before you lodge a lodge a ticket:

Ensure that you ask a question on our list, there might already be answer out there or we might have already acknowledged the issue

* Seek wisdom from our beautifully written documentation
* Google to see that it’s not something to do with your server environment (versions of Web server, WSGI connectors, etc)
* Check to ensure that you are not lodging a duplicate request.

When reporting issues:

Include as much detail as you can about your environment (e.g Server OS, Web Server Version, WSGI connector)

* Steps that we can use to replicate the bug
* Share a bit of your application code with us, it goes a long way to replicate issues


About the Authors
-----------------

prestans was developed by [Devraj Mukherjee](http://twitter.com/mdevraj, "Devraj Mukherjee on Twitter") and [Bradley Mclain](http://twitter.com/bradley_mclain, "Brad Mclain on Twitter") while building large scale Web applications at Eternity Technologies. These applications run on a Google's App Engine and servers running Apache + mod_wsgi.

We sometimes have things to say on our Twitter streams and are actively involved on our mailing list.

