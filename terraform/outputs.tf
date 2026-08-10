output "bucket_name" {
  value = google_storage_bucket.customer_bucket.name
}

output "dataset_id" {
  value = google_bigquery_dataset.customer_dataset.dataset_id
}

output "composer_bucket_name" {
  value = google_storage_bucket.composer_bucket.name
}

output "composer_environment_name" {
  value = google_composer_environment.customer_composer.name
}

output "composer_dag_gcs_prefix" {
  value = google_composer_environment.customer_composer.config[0].dag_gcs_prefix
}

output "composer_airflow_uri" {
  value = google_composer_environment.customer_composer.config[0].airflow_uri
}