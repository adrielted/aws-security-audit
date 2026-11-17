# AWS Security Audit

This is an AWS and Security Audit project. It uses Python (boto3) to detect misconfigurations in an AWS account. It generates alerts for each bucket of the account and for the roles that trust external accounts.

## Why I built this

I tried to recreate the idea of zSecure on a smaller scale, a tool that I worked with before in the mainframe environment, the idea is to find a wrong setting before it leaks or something goes wrong. And at the same time learn IAM in AWS.

## What it checks

| Check | Result | CIS v5.0.0 |
|---|---|---|
| Bucket's Public Access Block settings | OK if all four settings are True, ALERT if any of them is False | 2.1.4 (on Security Hub, the controls S3.1 and S3.8) |
| Roles that trust external accounts | REVIEW alert displaying role's name and external account ID | Related to 1.19 (IAM Access Analyzer enabled) |

## How to run

- Install python3 and AWS CLI v2 and clone the repository.

- Prepare the project: (only once)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install boto3 "botocore[crt]"
```
- Set your region: (you can find it in your AWS project info page)

```bash
aws configure set region <your-region> --profile lab
```

- Login to AWS: (once each 12 hours)

```bash
aws login --profile lab
```

- Run: 

```bash
python audit.py
```

## Example Output

```text
OK: adriel-audit-private-1611 is protected
ALERT: adriel-audit-test-1711 has a public access gap
REVIEW: AWSManagedAccountManagementAccessRole trusts external account 866746939446
REVIEW: AWSManagedAdvancedFeaturesActivationRole trusts external account 866746939446
```

## How I tested it

- First test: I created a second bucket (adriel-audit-test-1711) and turned off `BlockPublicPolicy` to run in both buckets and confirm that the script generates both OK and ALERT messages correctly.

- Second test: I added a temporary extra line -> account_id = "866746939446" and ran the code to show that it runs with no REVIEW alerts printed, comparing and proving that if the account_id is the same as mine it won't print, and if it's different it will detect as an external account. 

## Limitations

- The value of "AWS" can be a list of ARNs, an account number without ARN or even '*' (any, the most dangerous case).
- The `split(":")[4]` only works for ARN format.
- It doesn't read paginated `list_roles` (accounts with more than 100 roles).

