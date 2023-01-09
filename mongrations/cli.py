import click
import sys

# check python version
try:
    sys_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    min_required_version = "3.6"
    if int(sys_version[sys_version.index('.')+1:]) < int(min_required_version[min_required_version.index('.')+1:]):
        print(f"Python version 3.6 or greater is required to run mongrations. Your system version: {sys_version}")
        sys.exit(98)
except Exception:
    pass

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
    """Mongrations; a database independent migration and seeding tool for python. Compatible with MySQL, PostgreSQL and MongoDB."""
    pass


@cli.command()
def migrate():
    """Run migrations. The up() method will run on all migration files."""
    main.migrate()


@cli.command()
@click.argument('name', nargs=1)
@click.argument('directory', nargs=-1)
def create(name="no-name-migrations", directory="migrations"):
    """Create a new migration file. You can specify a name after the create command. You may also specify a directory name
    after the name argument."""
    if len(directory) > 0:
        directory = directory[0]
    else:
        directory = 'migrations'
    if len(name) == 0:
        name = 'no_name_migration'
    main.create(directory=directory, name=name)


@cli.command()
def undo():
    """Undo the last migration. Undo will run the down() method on the last migration
    file created and delete the migration file."""
    value = click.prompt("Are you sure you want to undo? (Y/n) ")
    if value.lower() == 'y':
        main.undo()


@cli.command()
def inspect():
    """Display the config file for mongrations. This will print a list of all migrations,
    the last migration file created/ran, etc."""
    main.inspector()


@cli.command()
@click.option("--all", default=False, help="Run down() method all migration files. This will not delete the migration files.")
def rollback(all):
    """Run the down() method on the last migration file. If --all is True the down()
    method will run on all migration files."""
    if all:
        main.down()
    else:
        main.down(last_migration_only=True)


if __name__ == '__main__':
    cli()
