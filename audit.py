import boto3

session = boto3.Session(profile_name="lab")
s3 = session.client("s3")
response = s3.list_buckets()

for bucket in response["Buckets"]:
    name = bucket["Name"]
    pab = s3.get_public_access_block(Bucket=name)
    if False in pab["PublicAccessBlockConfiguration"].values():
        print(f"ALERT: {name} has a public access gap")
    else:
        print(f"OK: {name} is protected")

sts = session.client("sts")
identity = sts.get_caller_identity()
account_id = identity["Account"]

iam = session.client("iam")
roles_response = iam.list_roles()

for role in roles_response["Roles"]:
    rolename = role["RoleName"]
    policy = role["AssumeRolePolicyDocument"]
    for statement in policy["Statement"]:
        principal = statement["Principal"]
        if "AWS" in principal:
            trusted_account = principal["AWS"].split(":")[4]
            if trusted_account != account_id:
                print(f"REVIEW: {rolename} trusts external account {trusted_account}")
                

            
            

