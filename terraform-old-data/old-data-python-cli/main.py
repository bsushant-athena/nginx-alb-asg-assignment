import fire
import logging
import shlex
import sys
from io import StringIO
from subprocess import Popen, PIPE, STDOUT

ec2instance_count_var=1
ec2instance_type="t2.micro"

init_cmd = "terraform init"
validate_cmd = "terraform validate"
output_cmd = "terraform output instance_ip_addr"
apply_cmd = "terraform apply -auto-approve"

logging.basicConfig(format='%(message)s', level=logging.INFO)

def log_subprocess_output(pipe):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logging.info('%r', line.rstrip())

def run_shell_command(cmd,logging):
    if logging:
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        with process.stdout:
            log_subprocess_output(process.stdout)
        exitcode = process.wait() # 0 means success

def deploy_autoscaling_nginx(ec2instance_count_var: int = 1,ec2instance_type: str = "t2.micro"):
    #verify input
    run_shell_command(init_cmd,True)
    print("Initialization is done.\n\n")
    run_shell_command(validate_cmd,True)
    print("Validation is done.\n\n")
    run_shell_command(apply_cmd,True)
    #error handlind
    print("Deployment is done.\n\n")
    run_shell_command(output_cmd,True)
    return


if __name__ == "__main__":
    fire.Fire({
        "deploy": deploy_autoscaling_nginx
    })