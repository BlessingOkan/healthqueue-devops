terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region                      = var.region
  access_key                  = "test"
  secret_key                  = "test"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3  = "http://localhost:4566"
    iam = "http://localhost:4566"
  }
}

resource "aws_s3_bucket" "build_artifacts" {
  bucket = "healthqueue-${var.app_name}-artifacts-${var.environment}"

  tags = {
    Project     = "HealthQueue"
    Environment = var.environment
    ManagedBy   = "OpenTofu"
  }
}

resource "aws_iam_role" "ci_pipeline" {
  name = "healthqueue-${var.app_name}-ci-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Project     = "HealthQueue"
    Environment = var.environment
    ManagedBy   = "OpenTofu"
  }
}
