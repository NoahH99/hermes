resource "aws_lambda_function" "update_ecs_service" {
  function_name = "update-ecs-service-desired-count"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  role          = var.lambda_exec_role_arn

  filename      = "./lambda/lambda_function.zip"

  vpc_config {
    subnet_ids         = [var.private_subnet_id]
    security_group_ids = [var.allow_egress_https_security_group_id]
  }
}

resource "aws_lambda_permission" "allow_eventbridge_start" {
  statement_id  = "AllowExecutionFromEventBridgeStart"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_ecs_service.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.start_ecs_service_arn
}

resource "aws_lambda_permission" "allow_eventbridge_stop" {
  statement_id  = "AllowExecutionFromEventBridgeStop"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_ecs_service.function_name
  principal     = "events.amazonaws.com"
  source_arn    = var.stop_ecs_service_arn
}
