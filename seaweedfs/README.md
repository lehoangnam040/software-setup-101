```
$ docker compose up -d
```

- Test with aws cli
```
$ vim .aws/credentials
[seaweedfs]
aws_access_key_id = namlh
aws_secret_access_key = verysecretpassword

$ aws --profile seaweedfs --endpoint-url http://localhost:8333 s3 mb s3://mybucket
$ aws --profile seaweedfs --endpoint-url http://localhost:8333 s3 ls mybucket/
```

- Ref: 
  - https://github-wiki-see.page/m/seaweedfs/seaweedfs/wiki/AWS-CLI-with-SeaweedFS
  - https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API