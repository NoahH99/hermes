resource "aws_cloudwatch_event_rule" "start_ecs_service" {
  name                = "start-ecs-service"
  schedule_expression = "cron(0 10 * * ? *)"
}

resource "aws_cloudwatch_event_rule" "stop_ecs_service" {
  name                = "stop-ecs-service"
  schedule_expression = "cron(30 1 * * ? *)"
}

resource "aws_cloudwatch_event_target" "start_target" {
  rule      = aws_cloudwatch_event_rule.start_ecs_service.name
  arn       = var.update_ecs_service_arn

  input = jsonencode({
    Service      = var.service_name,
    Cluster      = var.ecs_cluster_name,
    DesiredCount = 1
  })
}

resource "aws_cloudwatch_event_target" "stop_target" {
  rule      = aws_cloudwatch_event_rule.stop_ecs_service.name
  arn       = var.update_ecs_service_arn

  input = jsonencode({
    Service      = var.service_name,
    Cluster      = var.ecs_cluster_name,
    DesiredCount = 0
  })
}
