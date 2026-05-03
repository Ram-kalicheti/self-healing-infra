terraform {
  required_version = ">= 1.6"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "df47d210-ac7e-4a0b-985a-874cb3d27ea9"
}

resource "azurerm_resource_group" "main" {
  name     = "${var.cluster_name}-rg"
  location = var.location
}