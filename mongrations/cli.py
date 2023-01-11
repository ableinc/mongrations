import click
import sys
import json
import os
# check python version
try:
    sys_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    min_required_version = "3.6"
    if int(sys_version[sys_version.index('.')+1:]) < int(min_required_version[min_required_version.index('.')+1:]):
        click.echo(f"Python version 3.6 or greater is required to run mongrations. Your system version: {sys_version}")
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

def add_credentials_to_application_environment(service: str, credentials: dict) -> None:
    service_prefix = {
        "mongodb": "MONGO_",
        "mysql": "MYSQL_",
        "postgres": "POSTGRES_"
    }.get(service, None)
    for key in credentials:
        os.environ[f'{service_prefix}{key}'] = str(credentials[key])


def mongration_file_operation(file, env, service):
    try:
        with open(os.path.join(os.getcwd(), file)) as mf:
            mongration_file = json.load(mf)
    except FileNotFoundError:
        click.echo(f"The migration file, {file}, is not a file or is a directory.")
        sys.exit(86)
    try:
        credentials = mongration_file[env][service]
    except KeyError:
        click.echo("KeyError: Confirm the service name and env are valid.")
        sys.exit(86)
    add_credentials_to_application_environment(service, credentials)


@click.group()
@click.version_option(version=__version__)
def cli():
    """Mongrations; a database independent migration and seeding tool for python. Compatible with MySQL, PostgreSQL and MongoDB."""
    pass


@cli.command()
@click.option("--file", required=False, help="Pass a migration file with database credentials.")
@click.option("--env", default="development", required=False, help="Application environment. This is used with --file.")
@click.option("--service", required=False, help="The database service to use. Options: mongodb, mysql or postgres.")
def migrate(file, env, service):
    """Run migrations. The up() method will run on all migration files."""
    if file is not None and service is None:
        click.echo("You must provide the service name.")
        sys.exit(86)
    if file is not None:
        mongration_file_operation(file, env, service)
    main.migrate()


@cli.command()
@click.argument('name', nargs=1)
@click.argument('directory', nargs=-1)
def create(name, directory):
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
@click.argument('filename', nargs=1)
@click.option("--file", required=False, help="Pass a migration file with database credentials.")
@click.option("--env", default="development", required=False, help="Application environment. This is used with --file.")
@click.option("--service", required=False, help="The database service to use. Options: mongodb, mysql or postgres.")
def down(filename, file, env, service):
    """Run the down() method on a specified migration file"""
    if file is not None and service is None:
        click.echo("You must provide the service name.")
        sys.exit(86)
    if file is not None:
        mongration_file_operation(file, env, service)
    main.down(last_migration_only=False, specific_file=filename)


@cli.command()
@click.option("--file", required=False, help="Pass a migration file with database credentials.")
@click.option("--env", default="development", required=False, help="Application environment. This is used with --file.")
@click.option("--service", required=False, help="The database service to use. Options: mongodb, mysql or postgres.")
def undo(file, env, service):
    """Undo the last migration. Undo will run the down() method on the last migration
    file created and delete the migration file."""
    value = click.prompt("Are you sure you want to undo? (Y/n) ")
    if value.lower() == 'y':
        if file is not None and service is None:
            click.echo("You must provide the service name.")
            sys.exit(86)
        if file is not None:
            mongration_file_operation(file, env, service)
        main.undo()


@cli.command()
def inspect():
    """Display the config file for mongrations. This will print a list of all migrations,
    the last migration file created/ran, etc."""
    main.inspector()


@cli.command()
@click.option("--file", required=False, help="Pass a migration file with database credentials.")
@click.option("--env", default="development", required=False, help="Application environment. This is used with --file.")
@click.option("--service", required=False, help="The database service to use. Options: mongodb, mysql or postgres.")
@click.option("--all", default=False, help="Run down() method all migration files. This will not delete the migration files.")
def rollback(file, env, service, all):
    """Run the down() method on the last migration file. If --all is True the down()
    method will run on all migration files."""
    if file is not None and service is None:
        click.echo("You must provide the service name.")
        sys.exit(86)
    if file is not None:
        mongration_file_operation(file, env, service)
    if all:
        main.down()
    else:
        main.down(last_migration_only=True)

@cli.command()
def file():
    """Generate a mongrationFile.json at the root of the project directory."""
    main.create_mongration_file()


if __name__ == '__main__':
    cli()
