import click, os, sys
from mongrations.main import MongrationsCli
from mongrations.version import __version__


@click.command('mongrations')
@click.option('-M', '--migrate', default=False, type=click.BOOL,
              help='Run migrations')
@click.option('-C', '--create', default=False, type=click.BOOL,
              help='Create new migration')
@click.option('-N', '--name', default='-no-name-migration', type=click.STRING,
              help='Name for newly created migration')
@click.option('-F', '--file_path', default=os.getcwd(), type=click.STRING,
              help='File path for newly created migration')
@click.option('-U', '--undo', default=False, type=click.BOOL,
              help='Undo last migration')
@click.option('-D', '--down', default=False, type=click.BOOL,
              help='Revert database')
@click.version_option(version=__version__)
def mongrations(migrate, create, name, file_path, undo, down):
    main = MongrationsCli()
    if migrate:
        main.migrate()
        sys.exit()
    if create:
        main.create(file_path=file_path, name=name)
        sys.exit()
    if undo:
        main.undo()
        sys.exit()
    if down:
        main.down()
        sys.exit()


if __name__ == '__main__':
    mongrations()
