output "artifact_bucket_name" {
  description = "S3 bucket holding build artifacts (SBOMs, coverage, DORA exports)"
  value       = aws_s3_bucket.build_artifacts.bucket
}

output "ci_pipeline_role_arn" {
  description = "IAM role ARN the CI pipeline assumes"
  value       = aws_iam_role.ci_pipeline.arn
}

