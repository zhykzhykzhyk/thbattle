import gevent
from gevent import Greenlet
from gevent.event import Event
from gevent.queue import Queue
from functools import wraps
from utils import instantiate


@instantiate
class TransactionManager(Greenlet):
    def __init__(self):
        Greenlet.__init__(self)
        self.current = None
        self.commited = Queue(None)

    def _run(self):
        for trans in self.commited:
            trans.commit()

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
        if not self.started:
            self.start()

        self.current = None
        self.commited.put(trans)
        trans.wait()


class Transaction(object):
    def __init__(self):
        self.depth = 0
        self.thread = gevent.getcurrent()
        self.pending = []
        self.commited = Event()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.end()

    def begin(self):
        assert self.thread is gevent.getcurrent()
        assert not self.commited.is_set()
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
        self.commited.set()

    def wait(self):
        self.commited.wait()


def transactional(f):
    @wraps(f)
    def wrapper(*a, **k):
        with TransactionManager.begin():
            f(*a, **k)

    return wrapper
