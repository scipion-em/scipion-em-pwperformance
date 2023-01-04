=============
pwperformance
=============

**pwperformance** is a Scipion plugin with tests to measure performance and send benchmarks to a Codespeed server

Plugin installation
-------------------

.. code-block::

    git clone https://github.com/scipion-em/scipion-em-pwperformance.git
    scipion3 installp -p /path/to/scipion-em-pwperformance --devel

Environment variables
---------------------

Define the following environment vars:

.. code-block::

    CODESPEED_URL = Codespeed server URL to send benchmarks to. Defaults to "http://localhost:8000"
    CODESPEED_ENV = Environment name. Environment describes your testing PC configuration. Defaults to "unknown"
    CODESPEED_PROJECT = This should be the plugin you want to test. Defaults to "pyworkflow"
    CODESPEED_BRANCH = Git branch of your project. Defaults to "devel"
    CODESPEED_COMMIT = Git commit id of your project. Defaults to "1"

Codespeed server installation
-----------------------------

    #. conda create -y -n codespeed python=3.6
    #. conda activate codespeed
    #. pip3 install pypandoc==1.7.5 setuptools==57.5.0 gunicorn
    #. git clone https://github.com/tobami/codespeed
    #. cd codespeed
    #. pip3 install -e .
    #. pip3 install "django<2.2,>=1.11"
    #. python manage.py migrate
    #. python manage.py createsuperuser
    #. python manage.py runserver 8000
    #. Go to http://localhost:8000/admin
        #. create an environment (your CODESPEED_ENV)
        #. create a Github-type project (name = CODESPEED_PROJECT) with a correct url (e.g. https://github.com/scipion-em/scipion-pyworkflow), branch (e.g. "devel" or your own CODESPEED_BRANCH) and tick "Track changes"
        #. create a "devel" (or your own CODESPEED_BRANCH) branch

Example run
-----------

Run any of the following plugin tests to save the data on the codespeed server, e.g.:

.. code-block::

    scipion3 tests pwperformance.tests.test_profiling_load.TestProfilingLoadGUI
    scipion3 tests pwperformance.tests.test_set_performance.TestSetPerformanceSteps
    scipion3 tests pwperformance.tests.test_exportsteps.TestExportSteps