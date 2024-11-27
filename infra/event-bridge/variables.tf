variable "update_ecs_service_arn" {
  description = "The ARN of the lambda function to update ECS service."
  type = string
}

variable "ecs_cluster_name" {
  description = "The name of the ECS cluster."
  type        = string
}

variable "service_name" {
  description = "The name of the ECS service."
  type        = string
}
