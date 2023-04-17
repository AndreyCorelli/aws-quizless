resource "aws_vpc_endpoint" "quizless_vpc_endpoint" {
  vpc_id            = aws_vpc.quizless_vpc.id
  service_name      = "com.amazonaws.${var.aws_region}.s3"
  vpc_endpoint_type = "Gateway"
}

resource "aws_vpc_endpoint_route_table_association" "quizless_vpc_endpoint_route_table" {
  route_table_id  = aws_route_table.quizless_route_table.id
  vpc_endpoint_id = aws_vpc_endpoint.quizless_vpc_endpoint.id
}
