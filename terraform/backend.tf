terraform {
  backend "gcs" {
    bucket = "dauntless-loop-499615-j7-terraform-state"
    prefix = "terraform/state"
  }
}