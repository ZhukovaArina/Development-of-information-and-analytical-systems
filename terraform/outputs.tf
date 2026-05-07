output "vm_public_ip" {
  description = "Публичный IP виртуальной машины Airflow"
  value       = yandex_compute_instance.airflow_vm.network_interface.0.nat_ip_address
}

output "vm_internal_ip" {
  description = "Внутренний IP ВМ"
  value       = yandex_compute_instance.airflow_vm.network_interface.0.ip_address
}

output "s3_buckets" {
  description = "Имена созданных бакетов S3"
  value = [
    yandex_storage_bucket.raw.bucket,
    yandex_storage_bucket.bronze.bucket,
    yandex_storage_bucket.silver.bucket,
    yandex_storage_bucket.gold.bucket,
  ]
}

output "vpc_network_id" {
  description = "ID созданной сети VPC"
  value       = yandex_vpc_network.uni_network.id
}

output "subnet_id" {
  description = "ID созданной подсети"
  value       = yandex_vpc_subnet.uni_subnet.id
}
