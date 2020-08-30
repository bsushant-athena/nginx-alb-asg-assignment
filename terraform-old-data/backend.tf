terraform {
	backend "s3" {
	   bucket          = "perftest-logging"
	   key             = "terraform-dev-state/nginx-asg.tfstate"
	   region          = "us-east-1"
	   #dynamodb_table = "terraform-dev-state"
	   encrypt         = true
	}
}