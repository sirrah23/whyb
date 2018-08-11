#!/bin/bash
# Run tests for both front-end and back-end code.

frontend_tests () {
    pushd ./whyb_frontend
    npm run test:unit
    popd
}

backend_tests () {
    pushd ./whyb_backend
    pipenv run python -m unittest discover
    popd
}

frontend_tests
backend_tests 
