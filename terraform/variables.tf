variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "bucket_name" {
  type = string
}

variable "dataset_id" {
  type    = string
  default = "customer_dataset"
}

variable "composer_environment_name" {
  type    = string
  default = "customer-composer"
}

variable "composer_service_account" {
  type = string
}

variable "composer_bucket_name" {
  type = string
}