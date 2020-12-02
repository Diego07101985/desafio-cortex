# -*- coding: utf-8 -*-
import os

import click
from flask.cli import with_appcontext
from desafio.extensions import fpika
from desafio.consumers import ConsumerCurrency
import multiprocessing

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command('init-workers')
@with_appcontext
def init_workers():
    consumer = ConsumerCurrency(fpika.channel())
    consumer2 = ConsumerCurrency(fpika.channel())
    workers = 2
    pool = multiprocessing.Pool(processes=workers)
    pool.apply_async(
        consumer.receive_quotation_between_period_and_get_relation_currencys('relation.between.currencys', 'calc-relations'))
    pool.apply_async(
        consumer2.receive_quotation_between_period_and_get_relation_currencys('relation.between.currencys', 'calc-relations'))
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print(' [*] Exiting...')
        pool.terminate()
        pool.join()


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)
