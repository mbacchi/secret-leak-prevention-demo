provider "aws" {
  region = "us-west-2"
}

locals {
  user_data = <<-EOF
#!/bin/bash
cd /root
curl -O https://raw.githubusercontent.com/mbacchi/secret-leak-prevention-demo/master/aws-role-ec2-assumerole/terraform/write_time_to_s3.py

yum install -y python3.7
pip3 install --user boto3

echo "* * * * * root BUCKET_NAME=${aws_s3_bucket.demo_aws_role_ec2_assumerole.id} python3 /root/write_time_to_s3.py" >> /etc/cron.d/write_time_every_minute

EOF

}

resource "aws_s3_bucket" "demo_aws_role_ec2_assumerole" {
  acl = "private"

  bucket = "s3-bucket-test-ec2-assumerole-9so-uvnz"

  tags = {
    Name    = "demo_aws_role_ec2_assumerole"
    Purpose = "demo_aws_role_ec2_assumerole"
  }

  versioning {
    enabled = true
  }

  force_destroy = true
}

resource "aws_iam_role" "demo_aws_role_ec2_assumerole" {

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

}

# resource "aws_iam_policy" "demo_aws_role_ec2_assumerole" {

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": "sts:AssumeRole",
#       "Resource": "${aws_iam_role.demo_aws_role_ec2_assumerole.arn}"
#     }
#   ]
# }
# EOF

# }

resource "aws_iam_role_policy" "demo_aws_s3_write_role_policy" {
  role = aws_iam_role.demo_aws_role_ec2_assumerole.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": [
          "arn:aws:s3:::${aws_s3_bucket.demo_aws_role_ec2_assumerole.id}",
          "arn:aws:s3:::${aws_s3_bucket.demo_aws_role_ec2_assumerole.id}/*"
      ]
    }
  ]
}
EOF
}

# resource "aws_iam_role_policy_attachment" "demo_aws_role_ec2_assumerole" {
#   role       = aws_iam_role.demo_aws_role_ec2_assumerole.name
#   policy_arn = aws_iam_policy.demo_aws_role_ec2_assumerole.arn
# }

resource "aws_iam_instance_profile" "demo_instance_profile" {
  name = "demo_instance_profile"
  role = aws_iam_role.demo_aws_role_ec2_assumerole.name
}

resource "aws_instance" "ec2_demo" {
  ami                  = "ami-0e8c04af2729ff1bb" # Amazon Linux 2 AMI 2.0.20200207.1
  instance_type        = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.demo_instance_profile.name
  user_data            = base64encode(local.user_data)

  tags = {
    Name    = "demo_aws_role_ec2_assumerole"
    Purpose = "demo_aws_role_ec2_assumerole"
  }
}
