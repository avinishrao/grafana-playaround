
#Creating SNS_TOPIC
resource "aws_sns_topic" "ERR_TOPIC" {
  name = "ERR_TOPIC"
}

#Integrating the SNS
resource "aws_lambda_permission" "lambda_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_lambda_func.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.ERR_TOPIC.arn
}

#Subscribing to the SNS_TOPIC
resource "aws_sns_topic_subscription" "sns_subscription" {
  topic_arn = aws_sns_topic.ERR_TOPIC.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.email_lambda_func.arn
}