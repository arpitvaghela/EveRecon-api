#!/bin/bash

# sort imports and format codebase
isort . && black api

# run tests
echo "======== Running TEST ============"
cd api && python manage.py test

echo "======== DONE!! =================="