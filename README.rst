=============
pwperformance
=============

**pwperformance** is a Scipion plugin with tests to measure performance and send benchmarks to a codeSpeed server


The entire collection is licensed under the terms of the GNU Public License,
version 3 (GPLv3).

--------------------------------
Environment variables (optional)
--------------------------------

::

    CODESPEED_URL : Codespeed url to send benchmarks to. Defaults to  http://localhost:8000
    CODESPEED_ENV = Codespeed environment. Defaults to unknown
    CODESPEED_PROJECT = Codespeed project. Defaults to unknown
    CODESPEED_REVISION = Codespeed revision. Defaults to unknown

You may want to set URL and REVISION to get proper results


conda create -y -n codespeed python=3.6
conda activate codespeed
pip3 install pypandoc==1.7.5 setuptools==57.5.0 gunicorn
https://github.com/python/codespeed.git
cd codespeed
git checkout speed.python.org
pip3 install -e .
python manage.py migrate
python manage.py createsuperuser
Set SECRET_KEY in speed_python/settings.py
python manage.py loaddata codespeed/fixtures/testdata.json
python manage.py runserver 8000
http://localhost:8000/admin Create an environment and a project
