#Creating the lambda function
resource "aws_lambda_function" "email_lambda_func" {
 filename                       = "${path.module}/lambdaSourceCode/lambda_handler.zip"
 function_name                  = "Grafana_Lambda_Email"
 role                           = aws_iam_role.lambda_role.arn
 handler                        = "lambda_handler.lambda_handler"
 runtime                        = "python3.9"

 environment {
    variables = {
      GRAFANA_PWD	  = "avinish1234"
      GRAFANA_UNAME	= "admin"
      GRAFANA_URL	  = "http://35.154.192.43:3000/api"
      SNS_ARN	      = "arn:aws:sns:eu-central-1:533212200538:ERR_TOPIC"
      TS_DB	        = "Grafana_Logs"
      TS_TABLE	    = "request_data"
      API_TOKEN     = "eyJrIjoiMjI1Q2dybG5UbVRWNURjSmlaRmp6SzQ5bnlsaDlTMFYiLCJuIjoiZ3JhZmFuYV91cmxfYXBpIiwiaWQiOjF9"
      REGION_NAME   = "eu-central-1"
    }
  }

}