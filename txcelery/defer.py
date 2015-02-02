#!/usr/bin/env python
"""txcelery
Copyright Sentimens Research Group, LLC
2014
MIT License

Module Contents:
    - DeferredTask
    - CeleryClient
"""
from functools import wraps
from types import MethodType, FunctionType

from twisted.internet import defer
from celery import states
from celery.local import PromiseProxy
from celery.result import AsyncResult


class DeferredTask(defer.Deferred, object):
    """Subclass of `twisted.defer.Deferred` that wraps a
    `celery.local.PromiseProxy` (i.e. a "Celery task"), exposing the combined
    functionality of both classes.

    `DeferredTask` instances can be treated both like ordinary Deferreds and
    oridnary PromiseProxies.
    """
    def __init__(self, async_result, canceller=None):
        """Instantiate a `DeferredTask`.  See `help(DeferredTask)` for details
        pertaining to functionality.

        async_result : celery.result.AsyncResult
            AsyncResult to be monitored.  When completed or failed, the
            DeferredTask will callback or errback, respectively.

        canceller : None or callable
            See `help(twisted.internet.defer.Deferred)`
        """
        # Deferred is an old-style class
        defer.Deferred.__init__(self, canceller=canceller or self._canceller)

        self.task = async_result
        self._d = self._monitor_task(async_result)
        self._d.addCallbacks(self.callback, errback=self.errback)

    @staticmethod  # Canceller is explicitly passed Deferred to be cancelled
    def _canceller(self):
        self._d.cancel()

    @staticmethod
    @defer.inlineCallbacks
    def _monitor_task(async_result):
        """Wrapper that handles the actual asynchronous monitoring of the task
        state.
        """
        while async_result.state in states.UNREADY_STATES:
            yield

        if async_result.state == 'SUCCESS':
            defer.returnValue(async_result.result)
        elif async_result.state == 'FAILURE':
            async_result.maybe_reraise()
        elif async_result.state == 'REVOKED':
            raise defer.CancelledError('Task {0}'.format(async_result.id))
        else:
            raise ValueError(
                'Cannot respond to `{}` state'.format(async_result.state)
            )


class CeleryClient(object):
    """Decorator class that wraps a celery task such that any methods
    returning an Celery `AsyncResult` instance are wrapped in a
    `DeferredTask` instance.

    Instances of `CeleryClient` expose all methods of the underlying Celery
    task.

    Usage:

        @CeleryClient
        @app.task
        def my_task():
            # ...

    Note:  The `@CeleryClient` decorator must be callsed __after__ the
           `@app.task` decorator, meaning that the former must be __above__
           the latter.
    """
    def __init__(self, fn):
        if not isinstance(fn, PromiseProxy):
            raise TypeError('Wrapped function must be a Celery task.')

        self._fn = fn

    def __repr__(self):
        s = self._fn.__repr__().strip('<>')
        return '<CeleryClient {s}>'.format(s=s)

    def __call__(self, *args, **kw):
        return self._fn(*args, **kw)

    def __getattr__(self, attr):
        attr = getattr(self._fn, attr)
        if isinstance(attr, MethodType) or isinstance(attr, FunctionType):
            return self._wrap(attr)
        return attr

    @staticmethod
    def _wrap(method):
        @wraps(method)
        def wrapper(*args, **kw):
            res = method(*args, **kw)
            if isinstance(res, AsyncResult):
                return DeferredTask(res)
            return res
        return wrapper

__all__ = [CeleryClient, DeferredTask]
