import click
try:
    from mongrations.main import MongrationsCli
    from mongrations.version import __version__
except Exception:
    from .main import MongrationsCli
    from .version import __version__

main = MongrationsCli()

@click.group()
@click.version_option(version=__version__)
def cli():
    """Mongrations; a database migration tool for Python 3.6 and above."""
    pass


@cli.command()
def migrate():
    main.migrate()


@cli.command()
@click.argument('name', nargs=1)
@click.argument('directory', nargs=-1)
def create(name, directory):
    if len(directory) == 0:
        directory = 'migrations'
    
    if len(name) == 0:
        name = 'no-name-migration'
    main.create(directory=directory, name=name)


@cli.command()
def undo():
    main.undo()


@cli.command()
def down():
    main.down()


@cli.command()
def inspect():
    main.inspector()


if __name__ == '__main__':
    cli()
