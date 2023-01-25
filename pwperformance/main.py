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
    CODESPEED_BRANCH = "CODESPEED_BRANCH"
    CODESPEED_COMMIT = "CODESPEED_COMMIT"

    @classmethod
    def _getHost(cls):
        return getEnv(cls.CODESPEED_URL, "http://localhost:8000")

    @classmethod
    def _getEnvironment(cls):
        return getEnv(cls.CODESPEED_ENV, "unknown")

    @classmethod
    def _getProject(cls):
        return getEnv(cls.CODESPEED_PROJECT, "pyworkflow")

    @classmethod
    def _getBranch(cls):
        return getEnv(cls.CODESPEED_BRANCH, "devel")

    @classmethod
    def _getCommitId(cls):
        return getEnv(cls.CODESPEED_COMMIT, "1")

    @classmethod
    def getCodeSpeedClient(cls):
        if cls.__client is None:
            from .client import Client

            cls.__client = Client(cls._getHost(),
                                  environment=cls._getEnvironment(),
                                  project=cls._getProject())

        return cls.__client

    @classmethod
    def saveData(cls, instance, benchmark):
        """ Save benchmarks to a buffer.
        :param instance: instance of the test class (to obtain the test name used as executable)
        :param benchmark: Benchmark to be saved
        """
        cli = cls.getCodeSpeedClient()

        # kwargs list: environment, project, benchmark, branch, commitid,
        # revision_date, executable, result_date, result_value,
        # max, min, std_dev

        # get class name of a test
        executable = type(instance).__name__

        cli.add_result(
            executable=executable,
            commitid=cls._getCommitId(),
            branch=cls._getBranch(),
            benchmark=benchmark.name,
            result_value=benchmark.time)

    @classmethod
    def sendData(cls):
        """ Upload all results in one POST request. """
        cli = cls.getCodeSpeedClient()
        cli.upload_results()


# Currently not used
class CodespeedHandler(StreamHandler):

    def emit(self, record):

        try:
            benchmark = getattr(record, BENCHMARK, None)
            if benchmark is not None:
                codespeed.saveData(self, benchmark)
                codespeed.sendData()

        except Exception as e:
            print("Can't send metric to code speed server: %s" % e)


# Currently not used
def addCodeSpeedLogger():
    try:
        csHandler = CodespeedHandler()
        logger = logging.getLogger()
        logger.addHandler(csHandler)

    except Exception as e:
        print("Can't add codeSpeed logger: %s" % e)


class Timer:
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
