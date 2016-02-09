# Setting up keys
HIO_UNIT="hardening-ssh-tests/0"
UNIT_TO_TEST="ubuntu/0"
juju scp $HIO_UNIT:/home/ubuntu/.ssh/id_rsa.pub /tmp/id_rsa.pub
juju scp /tmp/id_rsa.pub $UNIT_TO_TEST:/tmp/
juju run --unit $UNIT_TO_TEST "\
    useradd -m -d /home/hiotest hiotest; \
    install -m 700 -o hiotest -d /home/hiotest/.ssh; \
    install -m 640 -o hiotest /tmp/id_rsa.pub /home/hiotest/.ssh/authorized_keys"

# Running a test

juju action do hardening-ssh-tests/0 run-test test-name=default/inspec/ target-ip=10.5.0.9
