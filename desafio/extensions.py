from desafio.flask_extension_pika import Pika as FPika
from flask_caching import Cache
from contextlib import contextmanager


cache = Cache()
fpika = FPika()


@contextmanager
def session_scope(expire=False):
    print('session')
