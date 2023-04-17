resource "aws_api_gateway_rest_api" "quizless_api" {
  name        = "quizless-api"
}

resource "aws_api_gateway_resource" "quiz_resource" {
  rest_api_id = aws_api_gateway_rest_api.quizless_api.id
  parent_id   = aws_api_gateway_rest_api.quizless_api.root_resource_id
  path_part   = "quiz"
}

resource "aws_api_gateway_method" "quiz_command_method" {
  rest_api_id   = aws_api_gateway_rest_api.quizless_api.id
  resource_id   = aws_api_gateway_resource.quiz_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "quiz_api_integration" {
  rest_api_id = aws_api_gateway_rest_api.quizless_api.id
  resource_id = aws_api_gateway_resource.quiz_resource.id
  http_method = aws_api_gateway_method.quiz_command_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.quizeless_lambda.invoke_arn
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.quizeless_lambda.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.quizless_api.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "quiz_api_deployment" {
  depends_on = [
    "aws_api_gateway_integration.quiz_api_integration"
  ]

  rest_api_id = aws_api_gateway_rest_api.quizless_api.id
  stage_name  = "prod"
}

module "api_gateway_enable_cors" {
  source = "squidfunk/api-gateway-enable-cors/aws"
  version = "0.3.3"

  api_id          = aws_api_gateway_rest_api.quizless_api.id
  api_resource_id = aws_api_gateway_resource.quiz_resource.id
}

output "api_endpoint" {
  value = aws_api_gateway_deployment.quiz_api_deployment.invoke_url
}