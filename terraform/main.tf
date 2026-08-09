resource "google_storage_bucket" "customer_bucket" {
  name     = var.bucket_name
  location = var.region

  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "customer_dataset" {
  dataset_id = var.dataset_id
  location   = var.region
}