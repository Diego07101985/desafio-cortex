# -*- coding: utf-8 -*-
import os

import click
from flask.cli import with_appcontext
from desafio.extensions import db, fpika
from desafio.services import ConsumerCurrency
from desafio.currency.model import Currency
from desafio.seeds import MAP_CURRENCYS
import multiprocessing
import time


HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command('init-workers')
@with_appcontext
def init_workers():
    consumer = ConsumerCurrency(fpika.channel())
    # consumer2 = ConsumerCurrency(fpika.channel())
    workers = 2
    pool = multiprocessing.Pool(processes=workers)
    pool.apply_async(consumer.receive_currencys_in_base_bbb('*.info'))
    # pool.apply_async(consumer2.receive_currencys_in_base_bbb('*.info'))
    # Stay alive
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print(' [*] Exiting...')
        pool.terminate()
        pool.join()


@ click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@ click.command()
@ with_appcontext
def seed():
    db.session.bulk_save_objects(Currency(simbol_currency=key,
                                          name_description=value
                                          ) for key, value in MAP_CURRENCYS.items())
    db.session.commit()
