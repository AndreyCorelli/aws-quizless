variable "aws_region" {
  default    = "eu-central-1"
  type       = string
}

variable "quizless_subnet_az" {
  default    = "eu-central-1a"
  type       = string
}

variable "bucket_name_site" {
  default    = "quizeless-bucket"
  type       = string
}

variable "bucket_name_data" {
  default    = "quizeless-bucket-data"
  type       = string
}


variable "quizless_subnet_cidr" {
  default    = "10.0.1.0/24"
  type       = string
}
