module "ecs" {
  source                             = "./ecs"
  aws_region                         = var.aws_region
  container_cpu                      = var.container_cpu
  container_env_vars                 = var.container_env_vars
  container_image                    = var.container_image
  container_memory                   = var.container_memory
  container_name                     = var.container_name
  ecs_cluster_name                   = var.ecs_cluster_name
  secret_name                        = var.secret_name
  service_desired_count              = var.service_desired_count
  service_name                       = var.service_name
  task_cpu                           = var.task_cpu
  task_family_name                   = var.task_family_name
  task_memory                        = var.task_memory
  ecs_execution_role_arn             = module.security.ecs_execution_role_arn
  ecs_task_role_arn                  = module.security.ecs_task_role_arn
  allow_http_https_security_group_id = module.security.allow_http_https_security_group_id
  public_subnet_id                   = module.vpc.public_subnet_id
}

module "event-bridge" {
  source = "./event-bridge"
  ecs_cluster_name = var.ecs_cluster_name
  service_name = var.service_name
  update_ecs_service_arn = module.lambda.update_ecs_service_arn
}

module "lambda" {
  source = "./lambda"
  lambda_exec_role_arn = module.security.lambda_exec_role_arn
  private_subnet_id = module.vpc.private_subnet_id
  allow_egress_https_security_group_id = module.security.allow_egress_https_security_group_id
  start_ecs_service_arn = module.event-bridge.start_ecs_service_arn
  stop_ecs_service_arn = module.event-bridge.stop_ecs_service_arn
}

module "security" {
  source             = "./security"
  http_https_sg_name = var.http_https_sg_name
  vpc_id             = module.vpc.vpc_id
}

module "vpc" {
  source                  = "./vpc"
  availability_zone       = var.availability_zone
  igw_name                = var.igw_name
  private_subnet_cidr     = var.private_subnet_cidr
  private_subnet_name     = var.private_subnet_name
  public_route_table_name = var.public_route_table_name
  public_subnet_cidr      = var.public_subnet_cidr
  public_subnet_name      = var.public_subnet_name
  vpc_cidr                = var.vpc_cidr
  vpc_name                = var.vpc_name
}
