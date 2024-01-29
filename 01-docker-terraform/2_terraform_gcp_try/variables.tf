variable "credentials" {
  description = "My Credentials"
  default = "./terraform-demo-412704-b7335cfc0b9a.json"
}

variable "project" {
  description = "Project"
  default     = "terraform-demo-412704"
}
variable "region" {
  description = "Project Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}
variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "demo_dataset"
}


variable "gcs_bucket_name" {
  description = "Bucket Storage Name"
  default     = "terraform-demo-412704-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}