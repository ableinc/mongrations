try:
  from mongrations.main import Mongrations, MongrationsCli
  from mongrations.database import Database
  from mongrations.version import __version__
except ImportError:
  from .main import Mongrations, MongrationsCli
  from .database import Database
  from .version import __version__


__all__ = [Mongrations, MongrationsCli, Database, __version__]