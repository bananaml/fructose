#!/bin/bash
pip3 install build
python3 -m build
python3 -m twine upload dist/* --skip-existing -u __token__ -p $PYPI_PASSWORD # use api key as password