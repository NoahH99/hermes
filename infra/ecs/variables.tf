variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "ecs_cluster_name" {
  description = "The name of the ECS cluster."
  type        = string
}

variable "task_family_name" {
  description = "The family name of the ECS task definition."
  type        = string
}

variable "task_cpu" {
  description = "The amount of CPU units for the ECS task."
  type        = string
}

variable "task_memory" {
  description = "The amount of memory for the ECS task."
  type        = string
}

variable "container_name" {
  description = "The name of the container."
  type        = string
}

variable "container_image" {
  description = "The Docker image for the container."
  type        = string
}

variable "container_cpu" {
  description = "The amount of CPU units for the container."
  type        = number
}

variable "container_memory" {
  description = "The amount of memory for the container."
  type        = number
}

variable "container_env_vars" {
  description = "Environment variables for the container."
  type        = map(string)
}

variable "secret_name" {
  description = "List of names for the AWS Secrets Manager secrets."
  type        = string
}

variable "service_name" {
  description = "The name of the ECS service."
  type        = string
}

variable "service_desired_count" {
  description = "The desired number of ECS service instances."
  type        = number
}

variable "ecs_execution_role_arn" {
  description = "The ARN of the created ECS execution role."
  type        = string
}

variable "ecs_task_role_arn" {
  description = "The ARN of the created ECS task role."
  type        = string
}

variable "public_subnet_id" {
  description = "The public subnet id."
  type        = string
}
variable "allow_http_https_security_group_id" {
  description = "The security group id."
  type        = string
}
