# Mongrations
![alt text](https://img.icons8.com/ios/50/000000/database-restore.png "Mongrations Logo")
A MongoDB migrations tool for Python 3.5+.

# Install
```bash
pip install --upgrade mongrations
```
or
```bash
git clone https://github.com/ableinc/mongrations.git
cd mongrations
pip install --upgrade .
```

# Use
Mongrations comes with a CLI Tool as well as a class for a pythonic migration approach

**CLI**
```bash
Usage: mongrations [OPTIONS]

Options:
  -M, --migrate BOOLEAN  Run MongoDB migrations
  -C, --create BOOLEAN   Create new MongoDB migration
  -N, --name TEXT        Name for newly created migration
  -F, --file_path TEXT   File path for newly created migration
  -U, --undo BOOLEAN     Undo last MongoDB migration
  -D, --down BOOLEAN     Clean MongoDB database
  --version              Show the version and exit.
  --help                 Show this message and exit.
```
**CLI Examples**
```bash
mongrations -C true --name [migration_name]  # create new migration
mongrations -M true  # run migrations
mongrations -D true  # tear down migrations
mongrations -U true  # undo last migration
```

**Mongrations Class**
```python
from mongrations import MongrationsCli

migrations = MongrationsCli()

migrations.create(file_path='file/path', name='file_name')
migrations.migrate()
migrations.down()
migrations.undo()
```
Run example migration in examples/ folder