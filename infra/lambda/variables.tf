variable "lambda_exec_role_arn" {
  description = "The ARN of the created Lambda exec role."
  type = string
}

variable "private_subnet_id" {
  description = "The ID of the private subnet."
  type = string
}

variable "allow_egress_https_security_group_id" {
  description = "The ID of the security group."
  type = string
}

variable "start_ecs_service_arn" {
  description = "The ARN of the eventbridge schedule."
  type = string
}
variable "stop_ecs_service_arn" {
  description = "The ARN of the eventbridge schedule."
  type = string
}
