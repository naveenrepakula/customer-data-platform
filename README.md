# Customer Data Platform

Production-style AWS Data Engineering project for DataNova Analytics.

## Purpose
The Customer Data Platform ingests customer files into S3, validates them using Lambda, transforms them using AWS Glue, stores processed data in S3, and exposes it through Athena.

## Current Status
Sprint 0: Repository foundation.

## Main Services
- Amazon S3
- AWS Lambda
- AWS Glue
- Amazon Athena
- Amazon CloudWatch
- IAM
- AWS SAM

## Local Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest
```

## First Lambda Test
```bash
python lambda/validation/handler.py
```
