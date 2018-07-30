resource "aws_iam_role" "iam_for_garden_controller_lambda" {
  name = "iam_for_garden_controller_lambda"
  path = "/"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": ["lambda.amazonaws.com"]
      }
    }
  ]
}
EOF
}
