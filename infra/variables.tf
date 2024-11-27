variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
}

##### ECS Module #####

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

##### Security Module #####

variable "http_https_sg_name" {
  description = "Name tag for the security group"
  type        = string
}

##### VPC Module #####

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "vpc_name" {
  description = "Name tag for the VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
}

variable "public_subnet_name" {
  description = "Name tag for the public subnet"
  type        = string
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
}

variable "private_subnet_name" {
  description = "Name tag for the private subnet"
  type        = string
}

variable "availability_zone" {
  description = "Availability zone for subnets"
  type        = string
}

variable "igw_name" {
  description = "Name tag for the internet gateway"
  type        = string
}

variable "public_route_table_name" {
  description = "Name tag for the public route table"
  type        = string
}
