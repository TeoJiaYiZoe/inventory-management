terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_dynamodb_table" "inventory_table" {
  name         = "Inventory"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "item_name"
    type = "S"
  }

  global_secondary_index {
    name            = "NameIndex"
    hash_key        = "item_name"
    projection_type = "ALL"
    write_capacity  = 1
    read_capacity   = 1
  }

  tags = {
    Environment = "Development"
    Application = "InventoryApp"
  }
}

# Output the table name for reference
output "dynamodb_table_name" {
  value = aws_dynamodb_table.inventory_table.name
}