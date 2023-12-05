
#Zip the source code directory
data "archive_file" "zip_the_python_code" {
 type        = "zip"
 source_dir  = "${path.module}/lambdaSourceCode/"
 output_path = "${path.module}/lambdaSourceCode/lambda_handler.zip"
}
