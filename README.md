# DevOps Platform API

An intermediate cloud and DevOps portfolio project showing how to build, secure, ship, and operate a containerized service. It is intentionally small enough to run locally while using production-style delivery practices.

## Architecture

```text
GitHub PR -> CI quality gates -> Docker build/Trivy scan -> GHCR
                                      |
                              Kubernetes deployment
                                      |
                          Service -> 2-5 replicas + HPA
                                      |
                         /health /ready /metrics
```

## Included capabilities

- Flask API with liveness, readiness, and Prometheus metrics endpoints
- Gunicorn production server and non-root, read-only container filesystem
- Docker Compose local environment
- Kubernetes Deployment, Service, HPA, probes, resource limits, and pod security
- Terraform-managed AWS ECR repository with immutable tags, encryption, scanning, and lifecycle cleanup
- GitHub Actions CI/CD: tests, Python compile check, Terraform validation, container build, Trivy scan, GHCR publishing, and Kubernetes manifest validation

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python app.py
```

Or run the production container:

```bash
docker compose up --build
curl http://localhost:5000/health
curl http://localhost:5000/metrics
```

## Deploy to Kubernetes

Update the image in `deploy/kubernetes/deployment.yaml` to your registry, then:

```bash
kubectl apply -f deploy/kubernetes/
kubectl -n devops-demo get pods,svc,hpa
kubectl -n devops-demo port-forward svc/devops-platform-api 8080:80
curl http://localhost:8080/ready
```

## Provision the image registry

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

The Terraform example provisions only the ECR image registry. Cluster networking and compute can be connected to an existing EKS cluster or added as a deliberate next module.

## Suggested project extensions

Add an EKS module, Helm chart, Argo CD GitOps promotion, Grafana dashboards, and an OPA policy gate as follow-up milestones.
