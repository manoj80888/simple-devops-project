# Troubleshooting Runbook — Simple DevOps Project

## 1. Purpose

This runbook provides initial diagnostic steps for common problems affecting the Flask application, Docker container, GitHub Actions pipelines and AWS deployment.

## 2. General Incident Procedure

For every incident:

1. Identify the failed component and the time the failure occurred.
2. Capture the error message and relevant logs.
3. Check the latest code commit and workflow run.
4. Investigate one failure at a time.
5. Apply the smallest appropriate correction.
6. Rerun the relevant tests or deployment.
7. Confirm application health before closing the incident.

Never publish AWS credentials, GitHub tokens, private keys or other secrets in issue reports or logs.

## 3. CI Pipeline Failure

**Symptoms:** The GitHub Actions CI workflow fails or automated tests do not pass.

**Checks:**

From PowerShell in the project root:

```powershell
git status
pytest
```

Review the failed GitHub Actions step for dependency installation, test collection or assertion errors.

**Resolution:**

- Confirm the virtual environment and required dependencies.
- Fix the failing code or tests.
- Run `pytest` again.
- Commit and push the reviewed correction.
- Confirm that CI passes before proceeding.

## 4. Docker Build Failure

**Symptoms:** The Docker image cannot be built.

**Checks:**

```powershell
docker --version
docker build -t simple-devops-app:troubleshooting .
```

**Resolution:**

- Confirm that Docker Desktop is running.
- Check the Dockerfile and `.dockerignore`.
- Verify that dependency files are present and readable.
- Review the build output for the first actual error.
- Rebuild after correcting the cause.

Remove the troubleshooting image when it is no longer needed:

```powershell
docker image rm simple-devops-app:troubleshooting
```

## 5. GitHub OIDC Authentication Failure

**Symptoms:** The deployment workflow fails at AWS credential configuration, often with `Not authorized to perform sts:AssumeRoleWithWebIdentity`.

**Checks:**

- Confirm that the GitHub repository variable `AWS_DEPLOY_ROLE_ARN` contains the intended IAM role ARN.
- Confirm that the AWS IAM OIDC provider exists for `token.actions.githubusercontent.com`.
- Verify the audience is `sts.amazonaws.com`.
- Compare the IAM trust policy's subject condition with the actual `sub` claim printed by the diagnostic workflow.
- Confirm the expected repository and branch are permitted.

**Resolution:**

Correct the trust policy or repository configuration as appropriate, then rerun the workflow. Do not broaden trust to all repositories simply to make authentication succeed.

## 6. Amazon ECR Push or Pull Failure

**Symptoms:** The image cannot be uploaded to ECR or EC2 cannot pull it.

**Checks:**

- Verify the AWS region and repository URI.
- Confirm the repository exists.
- Check the GitHub deployment role's image-publishing permissions.
- Check the EC2 instance role's ECR read permissions.
- Confirm that the image tag matches the commit being deployed.

On the EC2 instance, where authorized, inspect the SSM command output and Docker error messages.

**Resolution:**

Correct the registry URI, image tag, region or required IAM permissions. Avoid granting unrestricted permissions when a specific repository permission is sufficient.

## 7. Systems Manager Deployment Failure

**Symptoms:** The SSM deployment command fails, times out or cannot reach the EC2 instance.

**Checks in AWS Console:**

1. Open Systems Manager.
2. Select **Fleet Manager** or **Managed nodes**.
3. Confirm that the instance is online.
4. Open **Run Command** and inspect the relevant command's status and output.
5. Confirm that the EC2 instance has the required instance profile and network access to Systems Manager endpoints.

**Resolution:**

Restore the managed-node connection, correct the missing permissions or networking issue, and rerun deployment after confirming the cause.

## 8. Application Health Check Failure

**Symptoms:** The health endpoint returns an error, times out or cannot connect.

**Checks on the EC2 instance through an authorized session:**

```bash
docker ps -a
docker logs --tail 100 simple-devops-app
curl -i http://127.0.0.1:5000/health
```

**Resolution:**

- Confirm that the container is running.
- Inspect application logs for startup or runtime errors.
- Verify the container port mapping and application listener.
- Correct the underlying issue and redeploy.
- Recheck the health endpoint before declaring recovery.

## 9. Public Application Is Unreachable

**Symptoms:** The browser cannot open the application.

**Checks:**

- Confirm that EC2 is running.
- Verify the current public IP address.
- Confirm that the container and application are healthy.
- Review the EC2 security group and required inbound rules.
- Check host and container port mappings.

**Security note:** Port 5000 is suitable for this learning demonstration but should not be exposed broadly in a production environment. Prefer a controlled access path or a properly secured HTTPS endpoint.

## 10. Deployment Replaced the Container but Health Fails

The current deployment process tests a candidate container before replacing the running container. This reduces risk but is not a guarantee of automatic rollback after every failure.

**Response:**

1. Inspect the SSM command output.
2. Review the current container state and logs.
3. Identify the last known-good image tag.
4. Restore that image using an approved recovery procedure if necessary.
5. Verify application health and record the incident.

Do not delete the last known-good image until recovery requirements are satisfied.

## 11. AWS Cost Concern

**Symptoms:** AWS charges continue even when the application is not being used.

**Checks:**

- Review AWS Billing and Cost Management.
- Check EC2 instance state.
- Review EBS volumes, ECR image storage and other retained resources.
- Check whether public IPv4 addresses or other provisioned services are billable.

**Resolution:**

Stop EC2 when it is not needed. Delete only resources that have been identified as unnecessary and are safe to remove. Remember that stopping EC2 does not remove all storage or other service charges.

## 12. Incident Closure Checklist

- [ ] Root cause identified or documented.
- [ ] Corrective action applied.
- [ ] CI and relevant deployment checks passed.
- [ ] Application health verified.
- [ ] Relevant logs and evidence retained.
- [ ] Any temporary troubleshooting resources cleaned up.
- [ ] Follow-up improvements documented.
