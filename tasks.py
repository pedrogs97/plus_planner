"""
File with task to run in CLI
"""
from datetime import datetime

from invoke import task


@task
def tests(ctx):
    """
    Execute project tests
    """
    ctx.run("python manage.py test")


@task
def migrations(ctx):
    """
    Execute makemigrations and migrate to database
    """
    ctx.run("python manage.py makemigrations")
    ctx.run("python manage.py migrate_schemas --shared")


@task
def runserver(ctx, port=8000):
    """
    Execute local server
    """
    ctx.run(f"python manage.py runserver 0.0.0.0:{port}")


@task
def collect(ctx):
    """
    Execute collect static files
    """
    ctx.run("python manage.py collectstatic --noinput")


@task
def backup_db(ctx):
    """
    Execute backup from database
    """
    today_label = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ctx.run("mkdir -p _backups_db")
    ctx.run(
        f"python manage.py dumpdata --exclude contenttypes --indent=1 > _backups_db/backup_db_{today_label}.json"
    )
