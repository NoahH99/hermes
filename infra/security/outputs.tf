output "ecs_execution_role_arn" {
  value = aws_iam_role.ecs_execution_role.arn
}

output "ecs_task_role_arn" {
  value = aws_iam_role.ecs_task_role.arn
}

output "allow_http_https_security_group_id" {
  value = aws_security_group.allow_http_https.id
}

output "lambda_exec_role_arn" {
  value = aws_iam_role.lambda_exec_role.arn
}

output "allow_egress_https_security_group_id" {
  value = aws_security_group.allow_egress_https.id
}
