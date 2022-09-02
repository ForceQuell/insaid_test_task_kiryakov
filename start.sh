#!/bin/bash

PROJECT_PATH='/home/server/insaid_test_task_kiryakov'
export PYTHONPATH="$PROJECT_PATH/src"

pipenv run uvicorn main:app --host 0.0.0.0
