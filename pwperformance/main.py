import logging
import os
from collections import namedtuple
from datetime import datetime
from logging import StreamHandler

BENCHMARK = "benchmark"

Benchmark = namedtuple('Benchmark', ['name', 'time'])
def getEnv(envName, default):
    return os.environ.get(envName, default)


class codespeed:
    __client = None

    CODESPEED_URL = "CODESPEED_URL"
    CODESPEED_ENV = "CODESPEED_ENV"
    CODESPEED_PROJECT = "CODESPEED_PROJECT"
    CODESPEED_REVISION = "CODESPEED_REVISION"

    @classmethod
    def _getHost(cls):
        return getEnv(cls.CODESPEED_URL, "http://localhost:8000")

    @classmethod
    def _getEnvironment(cls):
        return getEnv(cls.CODESPEED_ENV, "undefined")

    @classmethod
    def _getProject(cls):
        return getEnv(cls.CODESPEED_PROJECT, "undefined")

    @classmethod
    def _getRevision(cls):
        return getEnv(cls.CODESPEED_REVISION, "undefined")

    @classmethod
    def getCodeSpeedClient(cls):
        if cls.__client is None:

            from codespeed_client import Client

            # kwargs passed to constructor are defaults

            cls.__client = Client(cls._getHost(), environment=cls._getEnvironment(), project=cls._getProject())

        return cls.__client

    @classmethod
    def sendData(cls, benchmark):
        cli = cls.getCodeSpeedClient()

        # kwargs list: environment, project, benchmark, branch, commitid, revision_date, executable,
        #              result_date, result_value, max, min, std_dev

        # kwargs passed to add_result overwrite defaults
        cli.add_result( executable="Scipion",
                        commitid="undefined",
                        branch=cls._getRevision(),
                        benchmark=benchmark.name,
                        result_value=benchmark.time)

        # Note: this upload all results in one request
        cli.upload_results()

# Currently not used
class CodespeedHandler(StreamHandler):

    def emit(self, record):

        try:
            benchmark = getattr(record, BENCHMARK, None)
            if benchmark is not None:
                codespeed.sendData(benchmark)

        except Exception as e:
            print("Can't send metric to code speed server: %s" % e)

# Currently not used
def addCodeSpeedLogger():
    try:

        csHandler= CodespeedHandler()

        logger = logging.getLogger()
        logger.addHandler(csHandler)

    except Exception as e:
        print ("Can't add codeSpeed logger: %s" % e)


class Timer(object):
    """ Simple Timer base in datetime.now and timedelta. """
    def __init__(self, msg=None):
        self._msg = msg

    def tic(self):
        self._dt = datetime.now()

    def getElapsedTime(self):
        return datetime.now() - self._dt

    def toc(self, message='Elapsed:'):
        print(message, "\t", self.getElapsedTime())

    def __enter__(self):
        self.tic()

    def __exit__(self, type, value, traceback):
        self.toc(self._msg)
