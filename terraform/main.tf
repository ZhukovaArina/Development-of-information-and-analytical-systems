terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.129.0"
    }
  }
  required_version = ">= 1.5"
}

provider "yandex" {
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  zone                     = var.zone
  service_account_key_file = pathexpand("~/.yc/uni-sa-key.json")
}

# ============================================
# S3 Object Storage — 4 бакета (с явными ключами s3-manager)
# ============================================

resource "yandex_storage_bucket" "raw" {
  bucket        = "uni-raw-data-${var.folder_id}"
  force_destroy = true
  access_key    = "YCAJEuCuy7uyLZmbtfBnzB3DK"
  secret_key    = "YCMfKxcoksG7qk1UJsEtwzD1Qb8O-xlNwloNAVqO"
}

resource "yandex_storage_bucket" "bronze" {
  bucket        = "uni-bronze-layer-${var.folder_id}"
  force_destroy = true
  access_key    = "YCAJEuCuy7uyLZmbtfBnzB3DK"
  secret_key    = "YCMfKxcoksG7qk1UJsEtwzD1Qb8O-xlNwloNAVqO"
}

resource "yandex_storage_bucket" "silver" {
  bucket        = "uni-silver-layer-${var.folder_id}"
  force_destroy = true
  access_key    = "YCAJEuCuy7uyLZmbtfBnzB3DK"
  secret_key    = "YCMfKxcoksG7qk1UJsEtwzD1Qb8O-xlNwloNAVqO"
}

resource "yandex_storage_bucket" "gold" {
  bucket        = "uni-gold-layer-${var.folder_id}"
  force_destroy = true
  access_key    = "YCAJEuCuy7uyLZmbtfBnzB3DK"
  secret_key    = "YCMfKxcoksG7qk1UJsEtwzD1Qb8O-xlNwloNAVqO"
}

# ============================================
# VPC Network + Subnet
# ============================================

resource "yandex_vpc_network" "uni_network" {
  name = "uni-network"
}

resource "yandex_vpc_subnet" "uni_subnet" {
  name           = "uni-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.uni_network.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

# ============================================
# Сервисный аккаунт для ВМ
# ============================================

resource "yandex_iam_service_account" "vm_sa" {
  name = "uni-vm-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "vm_sa_storage" {
  folder_id = var.folder_id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.vm_sa.id}"
}

# ============================================
# Виртуальная машина
# ============================================

resource "yandex_compute_instance" "airflow_vm" {
  name        = "airflow-vm"
  platform_id = "standard-v3"
  zone        = var.zone

  resources {
    cores  = 4
    memory = 16
  }

  boot_disk {
    initialize_params {
      image_id = "fd817i7o8012578061ra"  # Ubuntu 22.04 LTS v20250623
      size     = 50
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.uni_subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }

  service_account_id = yandex_iam_service_account.vm_sa.id
}
# ============================================
# Managed Service for Apache Kafka
# ============================================

resource "yandex_mdb_kafka_cluster" "uni_kafka" {
  name        = "uni-kafka-cluster"
  environment = "PRODUCTION"
  network_id  = yandex_vpc_network.uni_network.id
  subnet_ids  = [yandex_vpc_subnet.uni_subnet.id]

  config {
    version          = "3.6"
    brokers_count    = 1
    zones            = ["ru-central1-a"]
    assign_public_ip = false

    kafka {
      resources {
        resource_preset_id = "s2.micro"
        disk_type_id       = "network-hdd"
        disk_size          = 10
      }
      kafka_config {
        num_partitions             = 3
        default_replication_factor = 1
        message_max_bytes          = 1048588
        sasl_enabled_mechanisms    = ["SASL_MECHANISM_SCRAM_SHA_512"]
      }
    }
  }
}

resource "yandex_mdb_kafka_user" "producer" {
  cluster_id = yandex_mdb_kafka_cluster.uni_kafka.id
  name       = "producer"
  password   = "KafkaPass123!"
  permission {
    topic_name = "uni_events"
    role       = "ACCESS_ROLE_PRODUCER"
  }
}

resource "yandex_mdb_kafka_user" "consumer" {
  cluster_id = yandex_mdb_kafka_cluster.uni_kafka.id
  name       = "consumer"
  password   = "KafkaPass123!"
  permission {
    topic_name = "uni_events"
    role       = "ACCESS_ROLE_CONSUMER"
  }
}

resource "yandex_mdb_kafka_topic" "uni_events" {
  cluster_id          = yandex_mdb_kafka_cluster.uni_kafka.id
  name                = "uni_events"
  partitions          = 3
  replication_factor  = 1
}
