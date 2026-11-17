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
