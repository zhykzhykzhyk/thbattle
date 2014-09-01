import gevent
from functools import wraps
from utils import instantiate


@instantiate
class TransactionManager(object):
    def __init__(self):
        self.current = None

    def require(self):
        if not self.current:
            self.current = trans = Transaction()
        else:
            trans = self.current

        trans.begin()
        return trans

    def support(self):
        trans = self.current or DummyTransaction
        trans.begin()
        return trans

    def commit(self, trans):
        assert trans is self.current

        self.current = None
        trans.commit()


class Transaction(object):

    CONTEXT_CHECK = True

    def __init__(self):
        self.depth = 0
        self.context = gevent.getcurrent()
        self.callbacks = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()

    if CONTEXT_CHECK:
        def check(self):
            try:
                assert self.context is gevent.getcurrent(), 'Context switched in transaction'
            except AssertionError, e:
                self.context.kill(e)
                raise

    else:
        def check(self):
            pass

    def begin(self):
        self.check()
        self.depth += 1

    def end(self):
        self.check()
        assert self.depth > 0
        self.depth -= 1
        if self.depth == 0:
            TransactionManager.commit(self)

    if CONTEXT_CHECK == 'full':
        def on_commit(self, callback):
            self.check()
            self.callbacks.append(callback)
    else:
        def on_commit(self, callback):
            self.callbacks.append(callback)

    def commit(self):
        for cb in self.callbacks:
            cb()


@instantiate
class DummyTransaction(object):
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def begin(self):
        pass

    def end(self):
        pass

    def on_commit(self, callback):
        callback()

    def commit(self):
        pass


def transactional(f):
    @wraps(f)
    def wrapper(*a, **k):
        with TransactionManager.require():
            f(*a, **k)

    return wrapper
