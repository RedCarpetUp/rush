
###Setup
- make sure you are using python > 3.7+
- setup virtualenv using `virtualenv env` and activate it
- run `python setup.py install` to install dependencies. keep setup.py updated
  - rerun `python setup.py install` if you make changes to models/source code. not needed for testcase changes
- run `pytest --mypy` to run your tests
- all source code is under `src/rush/` . That is where you should make your code
