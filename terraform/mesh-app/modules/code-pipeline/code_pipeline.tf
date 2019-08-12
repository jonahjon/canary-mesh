resource "aws_codepipeline" "pipeline" {
  name     = "${var.name}"
  role_arn = "${aws_iam_role.codepipeline.arn}"

  artifact_store {
    location = "${aws_s3_bucket.codepipeline.bucket}"
    type     = "S3"
  }

  stage {
    name = "ECR_Trigger"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "ECR"
      version          = "1"
      output_artifacts = ["source"]

      configuration = {
        RepositoryName = "${var.repository}"
        ImageTag       = "${var.image_tag}"
      }
    }
  }

  stage {
    name = "Fetch_Templates"

    action {
      name             = "Fetch_Templates"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source"]
      output_artifacts = ["templates"]
      version          = "1"

      configuration = {
        ProjectName = "${var.name}"
      }
    }
  }

  stage {
    name = "Deploy_Image"

    action {
      name            = "Deploy"
      category        = "Deploy"
      owner           = "AWS"
      provider        = "CodeDeployToECS"
      input_artifacts = ["source", "templates"]
      version         = "1"
      configuration = {
        ApplicationName                = var.code_deploy_app_name
        DeploymentGroupName            = var.code_deploy_deployment_group_name
        AppSpecTemplateArtifact        = "templates"
        AppSpecTemplatePath            = "appspec.yml"
        TaskDefinitionTemplateArtifact = "templates"
        TaskDefinitionTemplatePath     = "task_def.json"
        Image1ArtifactName             = "source"
        Image1ContainerName            = "IMAGE"

      }
    }
  }

}
