# Standard Operating Procedure (SOP): Application Deployment

## 1. Document Information

| Field | Value |
|---|---|
| Application | Simple DevOps Project |
| Application type | Python Flask |
| Deployment platform | AWS EC2 |
| Container registry | Amazon ECR |
| Deployment mechanism | GitHub Actions and AWS Systems Manager |
| Procedure type | CI/CD deployment and verification |

## 2. Purpose

This procedure describes how to deploy a tested application version through the automated GitHub Actions pipeline and verify the result.

## 3. Prerequisites

Before starting, confirm that:

- The required code changes have been committed and pushed to the GitHub `main` branch.
- The GitHub Actions CI workflow is configured and enabled.
- The deployment workflow and AWS OIDC configuration are valid.
- The EC2 instance is running and registered as an online managed node in Systems Manager.
- The EC2 instance has the IAM permissions required to pull images from ECR.
- The deployment IAM role has the necessary ECR and SSM permissions.
- The required AWS resources exist in the configured region.

Do not store AWS credentials, tokens, or private keys in the repository.

## 4. Deployment Procedure

### Step 1 — Review the change

Review the code changes locally and confirm that only intended files are included.

From PowerShell in the project root:

```powershell
git status
git diff
```

### Step 2 — Run automated tests

Activate the project's virtual environment if necessary, then run:

```powershell
pytest
```

Do not proceed if tests fail.

### Step 3 — Commit and push

After reviewing and testing the changes:

```powershell
git add .
git commit -m "Describe the application change"
git push origin main
```

Review the staged changes before committing. Do not commit secrets, virtual-environment files, generated artifacts, or unrelated files.

### Step 4 — Verify continuous integration

Open the GitHub repository and select **Actions**.

Confirm that the CI Pipeline for the pushed commit completes successfully.

If CI fails, inspect the failing step and resolve the issue before deployment.

### Step 5 — Verify automated deployment

Open the Deploy to AWS workflow in GitHub Actions.

Confirm that the workflow:

- Authenticates to AWS successfully through OIDC.
- Builds and pushes the image to Amazon ECR.
- Sends the deployment command through Systems Manager.
- Reports successful deployment and health verification.

Use the workflow logs to investigate failures.

### Step 6 — Validate application health

When the EC2 instance is running, verify the health endpoint using the current public IP or another configured access path.

Example:

```powershell
Invoke-RestMethod "http://<EC2-PUBLIC-IP>:5000/health"
```

Replace `<EC2-PUBLIC-IP>` with the actual current public IP. Do not assume that a previously used public IP remains valid.

Confirm that the returned status indicates the application is healthy. Also check the main application page and relevant application behavior.

## 5. Rollback and Failure Handling

If a deployment fails:

1. Open the failed GitHub Actions job and identify the failing step.
2. Review the Systems Manager command output if deployment reached EC2.
3. Check the application container logs and health endpoint.
4. Preserve diagnostic output before changing resources.
5. If the new version is unhealthy, restore a previously verified image using an approved recovery procedure.
6. Confirm that the restored application passes its health check.

The deployment script performs a candidate health check before replacing the existing application. However, a failure after the replacement begins may still require manual recovery. Do not assume every failure automatically rolls back.

## 6. Post-Deployment Checks

- CI workflow is green.
- Deployment workflow is green.
- Application health endpoint responds successfully.
- Main application page loads.
- No unexpected container restarts or errors are observed.
- The deployed image tag matches the intended commit.
- Relevant deployment logs are retained.

## 7. Cost-Control Procedure

When testing is complete and the application is no longer needed:

1. Confirm that no further live testing or deployment is required.
2. Open AWS Console → EC2 → Instances.
3. Select the project instance.
4. Choose **Instance state → Stop instance**.
5. Confirm that its state becomes **Stopped**.

Do not terminate the instance unless permanent deletion is intended. EBS storage, ECR images, and other retained resources may continue to incur charges.

## 8. Troubleshooting Reference

| Problem | Initial action |
|---|---|
| CI failure | Inspect tests, dependencies and workflow logs. |
| OIDC authentication failure | Verify the IAM trust policy against the actual GitHub token claims. |
| ECR push failure | Verify the registry URI, region and role permissions. |
| SSM command failure | Check managed-node status, instance role and command output. |
| Health-check failure | Inspect container logs, port mappings and application configuration. |
| Public endpoint unreachable | Verify instance state, current IP and security-group rules. |

## 9. Completion Criteria

The deployment is considered successful only when the relevant CI and deployment workflows pass and the deployed application's health check succeeds.
