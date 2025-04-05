#!/bin/bash
cd "$(dirname "$0")"

source .venv/bin/activate

uvicorn main:API --reload --env-file .env
