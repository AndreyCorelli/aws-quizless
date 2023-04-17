resource "aws_elasticache_cluster" "quiz_cluster" {
  cluster_id           = "quiz-cluster"
  engine               = "redis"
  node_type            = "cache.t2.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis3.2"
  engine_version       = "3.2.10"
  port                 = 6379

  subnet_group_name    = aws_elasticache_subnet_group.elasticache_subnet_group.name
  security_group_ids   = [
    aws_security_group.quizeless_redis_security_group.id
  ]
}

resource "aws_elasticache_subnet_group" "elasticache_subnet_group" {
  name       = "elasticache-subnet-group"
  subnet_ids = [aws_subnet.quizless_private_subnet.id]
}

resource "aws_security_group" "quizeless_redis_security_group" {
  name        = "Quizless Redis security group"
  description = "Allow limited inbound traffic and unlimited outgoing traffic"
  vpc_id      = aws_vpc.quizless_vpc.id

  ingress {
    from_port        = 6379
    to_port          = 6379
    protocol         = "tcp"
    cidr_blocks      = [var.quizless_subnet_cidr]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Quizless Redis security group"
  }
}