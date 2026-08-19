variable "django_secret_key" {
  description = "Django secret key"
  type        = string
  sensitive   = true
}

variable "django_admin_username" {
  description = "Django admin username"
  type        = string
  sensitive   = true
}

variable "django_admin_password" {
  description = "Django admin password"
  type        = string
  sensitive   = true
}

variable "mysql_database" {
  description = "MySQL database name"
  type        = string
  sensitive   = true
}

variable "mysql_user" {
  description = "MySQL username"
  type        = string
  sensitive   = true
}

variable "mysql_password" {
  description = "MySQL password"
  type        = string
  sensitive   = true
}

variable "mysql_root_password" {
  description = "MySQL root password"
  type        = string
  sensitive   = true
}
variable "django_image" {
  description = "Django application container image"
  type        = string
  default     = "prapanjanprabhu/wrapzy:v4"
}

variable "django_node_port" {
  description = "NodePort exposed for django-service"
  type        = number
  default     = 32565
}

variable "mysql_image" {
  description = "MySQL container image"
  type        = string
  default     = "mysql:8.0"
}

variable "mysql_storage_class" {
  description = "StorageClass backing the MySQL PVC"
  type        = string
  default     = "standard"
}

variable "mysql_storage_size" {
  description = "Requested size of the MySQL PVC"
  type        = string
  default     = "1Gi"
}
