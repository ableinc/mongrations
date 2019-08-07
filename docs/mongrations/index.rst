Mongrations
=================================

Mongrations is a migration tool for Python 3.6+. Mongrations started as a MongoDB migrations tool but has introduced MySQL & Postgres
as compatible servers for the Mongrations tool. Later database adaptions could occur in the future. Mention it to us!

The goal of the project is to provide a simple way to introduce database management for projects that use Python as a
backend, such as Flask, Django & Sanic.


Mongrations is developed `on GitHub <https://github.com/ableinc/mongrations/>`_. Contributions are welcome!

Simple as simple gets
---------------------------

.. code:: python

    from mongrations import Mongrations, Database
    from pydotenv import load_env, load_env_object

    load_env()  # connect via environment variables (default)
    # config = load_env_object()  # connect via dictionary of environment variables [ i.e Mongrations(config) ]


    class Mongration(Database):
        def __init__(self):
            super(Database, self).__init__()

        def up(self):
            self.db['test_collection'].insert_one({'hello': 'world'})

        def down(self):
            self.db['test_collection'].delete_one({'hello': 'world'})


    Mongrations(Mongration, 'sync')

.. note::

    Mongrations does not support Python 3.5 or below. There are no plans in the near future to support this, but if an
    overwhelming majority of users require it, this could change.