output "namespace" {
  description = "Namespace all Wrapzy resources live in"
  value       = kubernetes_namespace.wrapzy.metadata[0].name
}

output "django_node_port" {
  description = "NodePort to reach Django on (minikube ip):(port)"
  value       = kubernetes_service.django.spec[0].port[0].node_port
}

output "mysql_service_host" {
  description = "In-cluster DNS name Django uses for the database"
  value       = kubernetes_service.mysql.metadata[0].name
}
