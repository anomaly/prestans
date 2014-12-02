## Prestans 2.0

A WSGI compliant REST micro-framework.

http://docs.prestans.org/en/2.0

prestans is a REST micro-framework built right on top of WSGI, designed perform and co-exists with other middleware and frameworks that you employ. Our target audience are developers building large REST backends for use with pure Ajax (using a framework like Google Closure) or mobile applications. prestans is designed for you to "take as much or as little" you like, although we do think that it all works really well together.

Reasons you might like prestans:

* Built right on top of WSGI, and designed ground up to fit in with other frameworks and middleware
* Strongly represent REST philosophies in the framework design, use of proper HTTP headers and verbs
* Support for multiple dialects, including formalised patterns for binary content 
* Handlers maps HTTP verbs to implemented class methods, complimented  with custom request parser and response writer (built on top of WebOb)
* Unforgivingly strict parsing of requests and responses to ensure data integrity
* Helper methods to ease transformation of persistent objects to REST responses
* Pluggable integration to authentication

prestans ensures that we provide extensive and useful documentation, published at available on [Read The Docs](http://docs.prestans.org "prestans documentation"). Sphinx source available on [Github](http://github.com/prestans/prestans-docs/ "Docs source").

We also offer a set of [client side tools](https://github.com/prestans/prestans-client/ "prestans client") to compliment Google Closure.

If you are still wondering prestans is a latin word meaning "excellent, distinguished, imminent." :)

### Getting Help

We recommend the use of our mailing lists as the primary way of getting help:

* [Discuss](http://groups.google.com/group/prestans-discuss "Discuss") used for general discussion.
* [Announce](http://groups.google.com/group/prestans-announce "Announce") used for release and security announcements


### Reporting Issues

We prefer the use of our [Issue Tracker on Github](https://github.com/prestans/prestans/issues "Issue Tracker"), to triage feature requests, bug reports.

Before you lodge a lodge a ticket:

* Seek wisdom from our comprehensive documentation
* Check to ensure that you are not lodging a duplicate request
* Google to see that it’s not something to do with your server environment (versions of Web server, WSGI connectors, etc)
* Ensure that you ask a question on our list, there might already be answer out there or we might have already acknowledged the issue

When reporting issues:

* Include as much detail as you can about your environment (e.g Server OS, Web Server Version, WSGI connector)
* Steps that we can use to replicate the bug
* Share a bit of your application code with us, it goes a long way to replicate issues


### About the Authors

prestans was developed and is maintained by [Devraj Mukherjee](http://twitter.com/mdevraj "Devraj Mukherjee on Twitter") and [Bradley Mclain](http://twitter.com/bradley_mclain "Brad Mclain on Twitter") while building large scale Web applications at Anomaly Software. These applications run on  Google's [App Engine](https://developers.google.com/appengine/ "Google AppEngine web site") or Linux servers running [Apache](http://httpd.apache.org "Apache official homepage") + [mod_wsgi](https://github.com/GrahamDumpleton/mod_wsgi "mod_wsgi on Github").

We sometimes have things to say on our Twitter streams and are actively involved on our [mailing list](http://groups.google.com/group/prestans-discuss "Discuss").

