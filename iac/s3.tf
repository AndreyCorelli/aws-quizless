resource "aws_s3_bucket" "quiz_bucket" {
  bucket = var.bucket_name_site
}

resource "aws_s3_bucket" "quiz_bucket_data" {
  bucket = var.bucket_name_data
}

resource "aws_s3_bucket_website_configuration" "quiz_bucket_config" {
  bucket = aws_s3_bucket.quiz_bucket.id
  index_document {
    suffix = "index.html"
  }
}

output "website_url" {
  value = "http://${aws_s3_bucket_website_configuration.quiz_bucket_config.website_endpoint}"
}

resource "aws_s3_bucket_policy" "quiz_bucket_policy" {
  bucket = aws_s3_bucket.quiz_bucket.id

  policy = templatefile("s3-policy.json", {bucket_arn = aws_s3_bucket.quiz_bucket.arn})
}

module "template_files_website" {
  source = "hashicorp/dir/template"
  base_dir = "../storage/website"
}

resource "aws_s3_bucket_object" "quiz_bucket_site_files" {
  for_each     = module.template_files_website.files

  bucket       = aws_s3_bucket.quiz_bucket.id
  key          = each.key
  source       = each.value.source_path
  content      = each.value.content
  content_type = each.value.content_type
  etag         = each.value.digests.md5
}

module "template_files_data" {
  source = "hashicorp/dir/template"
  base_dir = "../storage/quiz"
}

resource "aws_s3_bucket_object" "quiz_bucket_data_files" {
  for_each     = module.template_files_data.files

  bucket       = aws_s3_bucket.quiz_bucket_data.id
  key          = each.key
  source       = each.value.source_path
  content      = each.value.content
  content_type = each.value.content_type
  etag         = each.value.digests.md5
}
