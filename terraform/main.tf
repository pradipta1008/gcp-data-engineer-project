resource "google_project_service" "composer_api" {
  project = var.project_id
  service = "composer.googleapis.com"

  disable_on_destroy = false
}

# --------------------------------------------------
# ETL DATA BUCKET
# --------------------------------------------------

resource "google_storage_bucket" "customer_bucket" {
  name                        = var.bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  storage_class               = "STANDARD"
}

# --------------------------------------------------
# BIGQUERY DATASET
# --------------------------------------------------

resource "google_bigquery_dataset" "customer_dataset" {
  dataset_id = var.dataset_id
  location   = var.region
}

# --------------------------------------------------
# COMPOSER BUCKET
# --------------------------------------------------

resource "google_storage_bucket" "composer_bucket" {
  name                        = var.composer_bucket_name
  location                    = var.region
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}

# --------------------------------------------------
# COMPOSER SERVICE ACCOUNT PERMISSION
# --------------------------------------------------

resource "google_storage_bucket_iam_member" "composer_bucket_worker" {
  bucket = google_storage_bucket.composer_bucket.name
  role   = "roles/composer.worker"
  member = "serviceAccount:${var.composer_service_account}"
}

# --------------------------------------------------
# COMPOSER ENVIRONMENT
# --------------------------------------------------

resource "google_composer_environment" "customer_composer" {
  provider = google-beta

  name   = var.composer_environment_name
  region = var.region

  storage_config {
    bucket = google_storage_bucket.composer_bucket.name
  }

  config {
    software_config {
      image_version = "composer-3-airflow-2.11.1-build.11"
    }

    node_config {
      service_account = var.composer_service_account
    }

    workloads_config {
      worker {
        min_count  = 2
        max_count  = 2
        cpu        = 0.5
        memory_gb  = 2
        storage_gb = 10
      }
    }
  }

  depends_on = [
    google_project_service.composer_api,
    google_storage_bucket_iam_member.composer_bucket_worker
  ]
}

# --------------------------------------------------
# COMPOSER DAG
# --------------------------------------------------

resource "google_storage_bucket_object" "composer_dag" {
  name   = "dags/composer.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../dags/composer.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}

# --------------------------------------------------
# SCRIPTS
# --------------------------------------------------

resource "google_storage_bucket_object" "scripts_init" {
  name   = "dags/scripts/__init__.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../scripts/__init__.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}

resource "google_storage_bucket_object" "scripts_extract" {
  name   = "dags/scripts/extract.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../scripts/extract.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}

resource "google_storage_bucket_object" "scripts_load" {
  name   = "dags/scripts/load.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../scripts/load.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}

resource "google_storage_bucket_object" "scripts_pyspark" {
  name   = "dags/scripts/pyspark_job.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../scripts/pyspark_job.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}

resource "google_storage_bucket_object" "scripts_vertex_ai" {
  name   = "dags/scripts/vertex_ai.py"
  bucket = google_storage_bucket.composer_bucket.name
  source = "${path.module}/../scripts/vertex_ai.py"

  depends_on = [
    google_composer_environment.customer_composer
  ]
}