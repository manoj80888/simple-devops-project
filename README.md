# Simple DevOps Project — Automated CI/CD Deployment on AWS

## 1. Project Overview

This project demonstrates an end-to-end DevOps workflow for a Python Flask application. It uses GitHub for source control, GitHub Actions for continuous integration and deployment, Docker for containerization, Amazon ECR for image storage, and Amazon EC2 for application hosting.

The deployment workflow uses GitHub OIDC to obtain temporary AWS credentials and AWS Systems Manager (SSM) to execute deployment commands on the EC2 instance.

## 2. Objectives

- Build and test a Flask application.
- Automate application testing through GitHub Actions.
- Package the application as a Docker image.
- Publish versioned images to Amazon ECR.
- Deploy the application to EC2 through AWS Systems Manager.
- Verify application health after deployment.
- Apply least-privilege access principles where practical.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Application | Python, Flask |
| Automated tests | pytest |
| Source control | Git, GitHub |
| CI/CD | GitHub Actions |
| Containerization | Docker |
| Container registry | Amazon ECR |
| Compute | Amazon EC2 |
| Remote commands | AWS Systems Manager |
| CI/CD authentication | GitHub OIDC with AWS IAM |
| Infrastructure configuration | AWS Console and IAM policies |

## 4. Architecture

1. A developer commits and pushes code to the GitHub `main` branch.
2. The CI workflow installs dependencies and runs automated tests.
3. When CI succeeds, the deployment workflow checks out the tested commit.
4. GitHub Actions builds a Docker image and pushes it to Amazon ECR.
5. GitHub Actions uses OIDC to assume the configured AWS IAM deployment role.
6. AWS Systems Manager sends a deployment script to the EC2 instance.
7. The instance pulls the image, checks candidate application health, and replaces the running application if the candidate passes.
8. A production health check confirms whether the deployment succeeded.

## 5. Repository Structure

```text
simple-devops-project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── pytest.ini
├── docs/
├── tests/
│   └── test_app.py
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements-dev.txt
├── requirements.txt
├── run.py
└── README.md
```

*Note: The structure above describes the expected project layout. Verify the actual files in your repository and adjust this tree if necessary.*

## 6. Run Locally

Activate the Python virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install application and development dependencies:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Run the application:

```powershell
python run.py
```

Open `http://127.0.0.1:5000/` in your browser.

Run automated tests from the project root:

```powershell
pytest
```

## 7. Build and Run with Docker

Build the Docker image:

```powershell
docker build -t simple-devops-app:local .
```

Start the container:

```powershell
docker run --rm -d --name simple-devops-local -p 5000:5000 simple-devops-app:local
```

Test the health endpoint:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

Stop the local container:

```powershell
docker stop simple-devops-local
```

## 8. CI/CD Workflow

### Continuous Integration

The GitHub Actions CI workflow runs on code changes and validates the application using automated tests.

### Continuous Deployment

After successful CI, the deployment workflow:

- Checks out the tested commit.
- Authenticates to AWS through GitHub OIDC.
- Builds and pushes a commit-tagged Docker image to ECR.
- Sends deployment commands to EC2 through SSM.
- Performs candidate and production health checks.

Deployment requires correctly configured GitHub repository variables, AWS IAM permissions, an OIDC provider, an SSM-managed EC2 instance, and a reachable ECR repository.

## 9. AWS Resources

The project uses the following AWS resources:

- Amazon ECR repository: `simple-devops-app`
- EC2 application server
- IAM deployment role for GitHub Actions
- IAM instance role for EC2
- Systems Manager Run Command
- GitHub OIDC identity provider

AWS resources may incur charges. Stopping EC2 reduces compute charges, but EBS storage, ECR images, and other retained resources can still incur costs.

## 10. Security Considerations

- Use GitHub OIDC rather than long-lived AWS access keys in GitHub Actions.
- Restrict the IAM trust policy to the intended GitHub repository and branch.
- Grant only the AWS permissions required for deployment.
- Avoid committing credentials, private keys, access tokens, or `.env` files.
- Restrict inbound EC2 security-group rules to the minimum required access.
- Review ECR image retention and AWS billing regularly.

## 11. Troubleshooting

| Symptom | Initial checks |
|---|---|
| CI workflow fails | Review the failing test or dependency installation step. |
| AWS credential configuration fails | Check the OIDC provider, role ARN, trust policy and GitHub OIDC claims. |
| ECR push fails | Check repository URI, region and IAM permissions. |
| SSM command fails | Check instance state, SSM agent status, instance role and command output. |
| Health check fails | Check container logs, port mappings and application health endpoint. |
| Application is unreachable | Check EC2 state, current public IP and security-group rules. |

## 12. Future Improvements

- Manage AWS infrastructure with Terraform.
- Add CloudWatch logs, metrics and alarms.
- Add Docker image vulnerability scanning.
- Configure HTTPS using a domain and an appropriate TLS termination service.
- Add documented rollback and recovery procedures.
- Consider Kubernetes deployment as a separate learning enhancement.

## 13. Project Status

The core CI/CD deployment has been tested successfully, and the application health endpoint returned `{"status":"UP"}`. The EC2 instance was subsequently stopped to help control costs.

Further documentation, infrastructure automation, monitoring, and security improvements can be added incrementally.

## 14. Repository

GitHub: https://github.com/manoj80888/simple-devops-project
