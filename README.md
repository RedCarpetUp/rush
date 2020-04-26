
###Setup
- make sure you are using python > 3.7+
- setup virtualenv using `virtualenv env` and activate it
- run `python setup.py install` to install dependencies. keep setup.py updated
  - rerun `python setup.py install` if you make changes to models/source code. not needed for testcase changes
- run `pytest --mypy --black --isort` to run your tests
  - if black formatting tests fail, just run `black .` from your top level directory. Alternatively you can setup black in vscode (I highly recommend setting up all three ***"format on paste/save/type"***)
  - if isort formatting tests fail, just run `isort -rc .` from your top level directory.
- all source code is under `src/rush/` . That is where you should make your code
