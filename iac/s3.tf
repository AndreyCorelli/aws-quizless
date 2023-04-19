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

locals {
  server_js_path = "${path.module}/../website_src/js/server.js"
  new_quiz_api_url = replace(
    "${aws_api_gateway_deployment.quiz_api_deployment.invoke_url}/quiz/", "/", "\\/"
  )
}

resource "null_resource" "modify_server_js_file" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = "sed -i 's/_SERVER_URL_/${local.new_quiz_api_url}/g' ${local.server_js_path}"
  }
  depends_on = [aws_api_gateway_deployment.quiz_api_deployment]
}


module "template_files_website" {
  source = "hashicorp/dir/template"
  base_dir = "../website_src"
}

resource "aws_s3_bucket_object" "quiz_bucket_site_files" {
  for_each     = module.template_files_website.files

  bucket       = aws_s3_bucket.quiz_bucket.id
  key          = each.key
  source       = each.value.source_path
  content      = each.value.content
  content_type = each.value.content_type
  etag         = each.value.digests.md5

  depends_on   = [null_resource.modify_server_js_file]
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
