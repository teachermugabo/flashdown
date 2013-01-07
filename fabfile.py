"""Management utilities."""


from fabric.contrib.console import confirm
from fabric.api import abort, env, local, settings, task


########## GLOBALS
env.run = 'heroku run python manage.py'
HEROKU_ADDONS = (
    'cloudamqp:lemur',
    'heroku-postgresql:dev',
    'scheduler:standard',
    'memcache:5mb',
    'newrelic:standard',
    'pgbackups:auto-month',
    'sentry:developer',
)
HEROKU_CONFIGS = (
    'DJANGO_SETTINGS_MODULE=flashdown.settings.prod',
    'SECRET_KEY=dqm+gfarm4+d0bq9o*gxshoaz)ay2k1(gn$g(hesezvv#hld9y'
    'AWS_ACCESS_KEY_ID=xxx',
    'AWS_SECRET_ACCESS_KEY=xxx',
    'AWS_STORAGE_BUCKET_NAME=xxx',
)
########## END GLOBALS


########## HELPERS
def cont(cmd, message):
    """Given a command, ``cmd``, and a message, ``message``, allow a user to
    either continue or break execution if errors occur while executing ``cmd``.

    :param str cmd: The command to execute on the local system.
    :param str message: The message to display to the user on failure.

    .. note::
        ``message`` should be phrased in the form of a question, as if ``cmd``'s
        execution fails, we'll ask the user to press 'y' or 'n' to continue or
        cancel exeuction, respectively.

    Usage::

        cont('heroku run ...', "Couldn't complete %s. Continue anyway?" % cmd)
    """
    with settings(warn_only=True):
        result = local(cmd, capture=True)

    if message and result.failed and not confirm(message):
        abort('Stopped execution per user request.')
########## END HELPERS


########## DATABASE MANAGEMENT
@task
def syncdb():
    """Run a syncdb."""
    local('%(run)s syncdb --noinput' % env)


@task
def migrate(app=None):
    """Apply one (or more) migrations. If no app is specified, fabric will
    attempt to run a site-wide migration.

    :param str app: Django app name to migrate.
    """
    if app:
        local('%s migrate %s --noinput' % (env.run, app))
    else:
        local('%(run)s migrate --noinput' % env)
########## END DATABASE MANAGEMENT


########## FILE MANAGEMENT
@task
def collectstatic():
    """Collect all static files, and copy them to S3 for production usage."""
    local('%(run)s collectstatic --noinput' % env)

@task
def compress():
    """Pre-compress blocks, and copy the compressed files to S3."""
    local('%(run)s compress' % env)
########## END FILE MANAGEMENT


########## HEROKU MANAGEMENT
@task
def bootstrap(app=''):
    """Bootstrap your new application with Heroku, preparing it for a production
    deployment. This will:

        - Create a new Heroku application.
        - Install all ``HEROKU_ADDONS``.
        - Sync the database.
        - Apply all database migrations.
        - Initialize New Relic's monitoring add-on.
    """
    cont('heroku create %s' % app, "Couldn't create the Heroku app, continue anyway?")


    for addon in HEROKU_ADDONS:
        cont('heroku addons:add %s' % addon,
            "Couldn't add %s to your Heroku app, continue anyway?" % addon)

    for config in HEROKU_CONFIGS:
        cont('heroku config:add %s' % config,
            "Couldn't add %s to your Heroku app, continue anyway?" % config)

    cont('git push heroku master',
            "Couldn't push your application to Heroku, continue anyway?")

    syncdb()
    migrate()

    cont('%(run)s newrelic-admin validate-config - stdout' % env,
            "Couldn't initialize New Relic, continue anyway?")

    collectstatic()
    compress()

@task
def destroy(app=''):
    """Destroy this Heroku application. Wipe it from existance.

    .. note::
        This really will completely destroy your application. Think twice.
    """
    local('heroku apps:destroy %s' % app)

@task
def deploy():
    """Perform all necessary steps to deploy our app to Heroku."""
    cont('git push heroku master',
            "Couldn't push your application to Heroku, continue anyway?")
    syncdb()
    migrate()
    collectstatic()
    compress()

########## END HEROKU MANAGEMENT
