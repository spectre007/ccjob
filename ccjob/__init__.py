"""Top-level package for CompChemJob."""

__all__ = ['ccjob', 'queue', 'utils']
# deprecated to keep older scripts who import this from breaking
from ccjob.ccjob import Input, Job
from ccjob import queue
from ccjob import utils


__author__ = """Alexander Zech"""
__email__ = 'alexzech777@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.3'
