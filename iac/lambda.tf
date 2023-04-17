resource "aws_lambda_function" "quizeless_lambda" {
  filename      = "../lambda_output/lambda.zip"
  function_name = "quizeless_lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambdas/quiz_api_lambda.lambda_handler"

  source_code_hash = md5("../lambda_output/lambda.zip")

  runtime       = "python3.9"

  environment {
    variables = {
      REDIS_HOST      = "${aws_elasticache_cluster.quiz_cluster.cache_nodes[0].address}"
      STORAGE_TYPE    = "s3"
      BUCKET_NAME     = "quizeless-bucket-data"
      ALLOWED_ORIGINS = "*"
    }
  }

  vpc_config {
    subnet_ids         = [aws_subnet.quizless_private_subnet.id]
    security_group_ids = [aws_security_group.quizeless_lambda_security_group.id]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = file("lambda-assume-role.json")
}

resource "aws_iam_policy" "lambda_s3_policy" {
  name        = "lambda-s3-policy"
  description = "A policy enabling S3 for Lambda"
  policy      = templatefile("lambda_s3_policy.json", {bucket_arn = aws_s3_bucket.quiz_bucket_data.arn})
}

resource "aws_iam_role_policy_attachment" "s3_lambda_policy_attachment" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

resource "aws_iam_policy" "lambda_network_policy" {
  name        = "lambda-network-policy"
  description = "A policy enabling network actions for Lambda"
  policy      = file("lambda_network_policy.json")
}

resource "aws_iam_role_policy_attachment" "network_lambda_policy_attachment" {
  role       = "${aws_iam_role.iam_for_lambda.name}"
  policy_arn = aws_iam_policy.lambda_network_policy.arn
}

resource "aws_security_group" "quizeless_lambda_security_group" {
  name        = "Quizless Lambda security group"
  description = "Allow limited inbound traffic and unlimited outgoing traffic"
  vpc_id      = aws_vpc.quizless_vpc.id

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = [var.quizless_subnet_cidr]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Quizless Lambda security group"
  }
}