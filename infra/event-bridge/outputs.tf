output "start_ecs_service_arn" {
  value = aws_cloudwatch_event_target.start_target.arn
}

output "stop_ecs_service_arn" {
  value = aws_cloudwatch_event_target.stop_target.arn
}
