# DevOps CI/CD Demo

A small Flask service demonstrating a production-style GitHub Actions pipeline.

## What it includes

- Flask health-check service
- Automated tests with pytest
- Docker image build
- GitHub Actions workflow for pushes and pull requests to `main`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open <http://localhost:5000/health>.

## Run with Docker

```bash
docker build -t devops-ci-cd-demo .
docker run --rm -p 5000:5000 devops-ci-cd-demo
```

## Pipeline

The `CI` workflow runs tests first. The Docker build runs only after the tests pass, so pull requests and pushes provide a basic quality gate.
