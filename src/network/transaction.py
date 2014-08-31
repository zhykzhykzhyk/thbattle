import gevent
from functools import wraps
from utils import instantiate


@instantiate
class TransactionManager(object):
    def __init__(self):
        self.current = None

    def begin(self):
        if not self.current:
            self.current = trans = Transaction()
        else:
            trans = self.current

        trans.begin()
        return trans

    def end(self):
        self.current.end()

    def commit(self, trans):
        assert trans is self.current

        self.current = None
        trans.commit()


class Transaction(object):
    def __init__(self):
        self.depth = 0
        self.thread = gevent.getcurrent()
        self.pending = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()

    def begin(self):
        assert self.thread is gevent.getcurrent()
        self.depth += 1

    def end(self):
        assert self.depth > 0
        assert self.thread is gevent.getcurrent()
        self.depth -= 1
        if self.depth == 0:
            TransactionManager.commit(self)

    def add_pending(self, callback):
        self.pending.append(callback)

    def commit(self):
        for cb in self.pending:
            cb()


def transactional(f):
    @wraps(f)
    def wrapper(*a, **k):
        with TransactionManager.begin():
            f(*a, **k)

    return wrapper
