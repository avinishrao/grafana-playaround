
#Creating the lambda function
resource "aws_lambda_function" "lambda_func_conf" {
 filename                       = "${path.module}/lambdaSourceCode/lambda_handler.zip"
 function_name                  = "Grafana-Lambda-API-Function"
 role                           = aws_iam_role.lambda_role.arn
 handler                        = "lambda_handler.lambda_handler"
 runtime                        = "python3.9"
}
