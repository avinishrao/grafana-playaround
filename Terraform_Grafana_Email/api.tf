#Defining the API Gateway
resource "aws_apigatewayv2_api" "Grafana_API_Email" {
  name          = "Grafana_API_Email"
  protocol_type = "HTTP"
}
#Setting up the api call environment
resource "aws_apigatewayv2_stage" "Grafana_API_Email" {
  api_id = aws_apigatewayv2_api.Grafana_API_Email.id

  name        = "GrafanaURL_Email"
  auto_deploy = true
}
#Adding the API Gateway to the cloudwatch
resource "aws_cloudwatch_log_group" "GrafanaEmail_api_gw" {
  name = "/aws/api-gw/${aws_apigatewayv2_api.Grafana_API_Email.name}"

  retention_in_days = 14
}

#Integrating the API
resource "aws_apigatewayv2_integration" "api_integrate" {
  api_id = aws_apigatewayv2_api.Grafana_API_Email.id

  integration_uri    = aws_lambda_function.email_lambda_func.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}
#Defining the routes
resource "aws_apigatewayv2_route" "any" {
  api_id = aws_apigatewayv2_api.Grafana_API_Email.id

  route_key = "ANY /"
  target    = "integrations/${aws_apigatewayv2_integration.api_integrate.id}"
}

#Defining permissions for api
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_lambda_func.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.Grafana_API_Email.execution_arn}/*/*"
}