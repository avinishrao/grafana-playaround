#Defining the IAM Role & different access policy for lambda
resource "aws_iam_role" "lambda_role" {
  name                = "lambda_role_org"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  managed_policy_arns = [aws_iam_policy.policy_one.arn, aws_iam_policy.policy_two.arn, aws_iam_policy.policy_three.arn, aws_iam_policy.policy_four.arn]
}

resource "aws_iam_policy" "policy_one" {
  name = "policy-1"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "arn:aws:logs:*:*:*",
        "Effect": "Allow"
      }
    ]
  })
}

resource "aws_iam_policy" "policy_two" {
  name = "policy-2"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "sns:*",
        "Resource": "*"
      }
    ]
  })
}

resource "aws_iam_policy" "policy_three" {
  name = "policy-3"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "timestream:*",
        "Resource": "*"
      }
    ]
  })
}

resource "aws_iam_policy" "policy_four" {
  name = "policy-4"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Id": "key-policy",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": "kms:Encrypt",
        "Resource": "*"
      }
    ]
  })
}