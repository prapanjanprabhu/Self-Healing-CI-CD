resource "kubernetes_secret" "django" {
  metadata {
    name      = "django-secret"
    namespace = kubernetes_namespace.wrapzy.metadata[0].name
  }

  type = "Opaque"

  data = {
    DJANGO_SECRET_KEY = var.django_secret_key
    ADMIN_USERNAME    = var.django_admin_username
    ADMIN_PASSWORD    = var.django_admin_password
  }
}

resource "kubernetes_secret" "mysql" {
  metadata {
    name      = "mysql-secret"
    namespace = kubernetes_namespace.wrapzy.metadata[0].name
  }

  type = "Opaque"

  data = {
    MYSQL_DATABASE      = var.mysql_database
    MYSQL_USER          = var.mysql_user
    MYSQL_PASSWORD      = var.mysql_password
    MYSQL_ROOT_PASSWORD = var.mysql_root_password
  }
}
