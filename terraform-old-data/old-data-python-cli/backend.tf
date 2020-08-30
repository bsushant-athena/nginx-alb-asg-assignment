terraform {
	backend "s3" {
	   bucket          = "perftest-logging"
	   key             = "terraform-dev-state/ec2instance.tfstate"
	   region          = "us-east-1"
	   #dynamodb_table = "terraform-dev-state"
	   encrypt         = true
	}
}