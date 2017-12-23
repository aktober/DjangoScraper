from __future__ import absolute_import, unicode_literals
import os
import subprocess

import celery
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoScraper.settings')

app = Celery('coin-a')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = 'redis://localhost:6379/0'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls run_spider every 30 seconds.
    # sender.add_periodic_task(30.0, run_spider, name='starting spider')

    # Executes every Saturday morning at 10:00 a.m.
    sender.add_periodic_task(
        crontab(hour=10, minute=0, day_of_week=6),
        run_spider,
    )


if __name__ == '__main__':
    app.start()


@app.task
def run_spider():
    subprocess.call(['sh', 'scrape.sh'])


@celery.task
def run_task():
    print('run test task')
    from scraper.spiders.news_reddit import crawl
    return crawl()
