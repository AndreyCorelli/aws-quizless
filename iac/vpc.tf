resource "aws_vpc" "quizless_vpc" {
  cidr_block       = "10.0.0.0/16"

  tags = {
    Name = "quizless-vpc"
  }
}

resource "aws_route_table" "quizless_route_table" {
  vpc_id = aws_vpc.quizless_vpc.id

  tags = {
    Name = "quizless-route-table"
  }
}

resource "aws_subnet" "quizless_private_subnet" {
  vpc_id            = aws_vpc.quizless_vpc.id
  cidr_block        = var.quizless_subnet_cidr
  availability_zone = var.quizless_subnet_az

  tags = {
    Name = "quizless-private-subnet"
  }
}

resource "aws_route_table_association" "quizless_association" {
  subnet_id      = aws_subnet.quizless_private_subnet.id
  route_table_id = aws_route_table.quizless_route_table.id
}