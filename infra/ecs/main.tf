##### Clusters #####

resource "aws_ecs_cluster" "main" {
  name = var.ecs_cluster_name
}

##### Task Definitions #####

resource "aws_ecs_task_definition" "hermes_task" {
  family             = var.task_family_name
  cpu                = var.task_cpu
  memory             = var.task_memory
  network_mode       = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn = var.ecs_execution_role_arn
  task_role_arn      = var.ecs_task_role_arn

  container_definitions = jsonencode([
    {
      name        = var.container_name
      image       = var.container_image
      cpu         = var.container_cpu
      memory      = var.container_memory
      essential   = true
      environment = [
        for key, value in var.container_env_vars : {
          name  = key
          value = value
        }
      ]
      secrets = [
        {
          name      = "SECRETS"
          valueFrom = data.aws_secretsmanager_secret_version.prod_hermes_version.arn
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ecs_task_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

##### Services #####

resource "aws_ecs_service" "hermes_service" {
  name            = var.service_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.hermes_task.arn
  desired_count   = var.service_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets = [var.public_subnet_id]
    security_groups = [var.allow_http_https_security_group_id]
    assign_public_ip = true
  }
}


##### Cloud Watch Log Groups #####

resource "aws_cloudwatch_log_group" "ecs_task_logs" {
  name              = "/ecs/${var.ecs_cluster_name}/task-logs"
  retention_in_days = 7

  tags = {
    Name = "ECS Task Logs"
  }
}

##### Data #####

data "aws_caller_identity" "current" {}

data "aws_secretsmanager_secret" "prod_hermes" {
  name = var.secret_name
}

data "aws_secretsmanager_secret_version" "prod_hermes_version" {
  secret_id = data.aws_secretsmanager_secret.prod_hermes.id
}
