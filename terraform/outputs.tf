output "bucket_name" {
  value = google_storage_bucket.customer_bucket.name
}

output "dataset_id" {
  value = google_bigquery_dataset.customer_dataset.dataset_id
}