txCelery
=============

Celery for Twisted:  manage Celery tasks from twisted using the Deferred API

[![PyPI version](https://badge.fury.io/py/txCelery.svg)](http://badge.fury.io/py/txCelery)

##Deprecation Notice

txCelery is no longer being developed.  Open an issue if you would like to maintain the project.

## Motivation

Celery is an outstanding choice for dispatching *short-lived*, computationally-expensive tasks to a distributed backend system.  Note the emphasis; Celery is ill-suited for tasks tasks that require updating some in-memory representation with out-of-process data.  If you want a specific process to read data from standard input, for instance, good luck...

Twisted can be though of as having the opposite problem.  Twisted is very good at maintaining and updating in-memory representations over extended periods of time, but fails miserably at performing expensive computations.  Twisted notably has no built-in constructs for managing distributed task queues.

As its name suggests, txCelery elegantly couples these two frameworks together, and in so doing allows them to compliment each other.  Developers can now create long-running processes whose expensive subroutines can be farmed out to a distributed computational cluster.

And best of all, txCelery fully leverages Twisted's Deferred API, so there's no need to drink yet *another* framework's Koolaid.

## Installation

**Note**:  These instructions assume you have a working installation of [Celery](http://www.celeryproject.org/).

The recommended way of installing txCelery is through `pip`.  PyPI will contain the latest stable version of txCelery.

### Stable

First, install pip.  On Debian/Ubuntu systems, this is achieved with the `sudo apt-get install python-pip` command.

Next, let's install the latest stable version of txCelery:

- `pip install txCelery --user` to install for your user
- `sudo pip install txCelery` to install system-wide

### Development

The latest development files can be obtained by cloning the github repo, checking out the `dev` branch, and running `python setup.py develop --user`.  It is **strongly** recommended that you **do not** use the development version in production.

## Use

txCelery's API is so simple it brings tears to our eyes.  There are exactly one and a half constructs.  Yes, one and *one half*.

###The "one" construct:  wrapping a Celery task

In order to use a Celery task with Twisted, you must wrap your Celery task with a `CeleryClient`-class decorator.  In your `tasks.py` (or wherever you keep your Celery tasks):

```python
from celery import Celery
from txcelery.defer import CeleryClient

app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')


@CeleryClient
@app.task
def my_task(*args, **kw):
	# do something
```

There's just one thing to bear in mind:  contrary to the Celery documentation's insistance that `@app.task` be the top-most decorator in your function definition, `CeleryClient` expects to wrap a celery task and will throw a `TypeError` if it receives anything else.

Once you've wrapped your task with the `CeleryClient`-class decorator, you'll find all the usual task methods like `delay`, `apply_async`, `subtask`, `chain`, etc.  The difference is that those which used to return a `celery.result.AsyncResult` will now return a `twisted.internet.defer.Deferred` instance when they are called (ok, actually a subclass of `Deferred`, but more on that in a second).

###The "one half":  a (Deferred) rose by any other name...

So what of this subclass of Twisted's `Deferred`?  It can be thought of as a `Deferred` that also gives transparent access to all the attributes and methods of it's associated `AsyncResult` instance.  It can be thought of in those terms because that's *exactly what it is*, and that's why this part of the API only constitutes half of a thing to learn.

Our subclass is called `DeferredTask`, it lives in `txcelery.defer` and as far as Twisted is concerned it's just a plain old `Deferred`.  DeferredTasks can be chained, passed to `maybeDeferred`, joined via `gatherResults` and `DeferredList`, etc.

`DeferredTask` monitors the state of the task and fires with a callback if the task succeeds, or with an errback if the task fails.  If the task is revoked, `DeferredTask` fires with an errback containing a `twisted.defer.CancelledError` as it's `Failure` value.

###In summary

1.  Wrap a task with a `CeleryClient`
2.  Call task methods and obtain a `DeferredTask` instance in lieu of an `AsyncResult`
3.  Use `DeferredTask` as if it were a regular `Deferred` or a regular `AsyncResult`

And that's *really* all there is to it.
