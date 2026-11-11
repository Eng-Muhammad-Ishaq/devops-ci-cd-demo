output "ecr_repository_url" {
  description = "Push images to this ECR repository."
  value       = aws_ecr_repository.api.repository_url
}
