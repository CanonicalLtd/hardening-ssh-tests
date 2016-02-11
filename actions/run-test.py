#!/usr/bin/python3

from charmhelpers.core.hookenv import action_get, action_set
import subprocess

def run_test():
    action_config = action_get()
    priv_key_file = '/home/ubuntu/.ssh/id_rsa'
    base_cmd = 'bundle exec inspec exec'
    test_cmd = base_cmd +' {} -t ssh://hiotest@{} --key-files={}'.format(
        action_config['test-name'],
        action_config['target-ip'],
        priv_key_file
    )
    try:
        output  = subprocess.check_output(test_cmd.split(),
                                          stderr=subprocess.STDOUT,
                                          cwd='/srv/hardening/ssh/')
        returncode = 0
    except subprocess.CalledProcessError as ex:
        output = ex.output
        returncode = ex.returncode
    action_set({'test-output': output.decode('utf-8')})

if __name__ == '__main__':
    run_test()
