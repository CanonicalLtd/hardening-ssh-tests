from charms.reactive import (
  is_state, set_state,
  when, when_not,
  hookenv, hook,
)
from charmhelpers.core.hookenv import config
from subprocess import check_call
from charmhelpers.fetch import apt_install, apt_update
from rubylib import bundle
import os
import stat
import pwd

try:
    from Crypto.PublicKey import RSA
except ImportError:
    apt_update()
    apt_install('python3-crypto')
    from Crypto.PublicKey import RSA

@when('ruby.available')
def setup_tests():
    apt_install(['git'])
    if not os.path.exists(config('app-path')):
        clone()
    bundle('install')
    gen_sshkey()

def clone():
    cmd =  "git clone {} {}".format('https://github.com/hardening-io/tests-ssh-hardening.git', config('app-path'))
    res = check_call(cmd, shell=True)
    if res != 0:
      status_set('error', 'has a problem with git, try `resolved --retry')
      sys.exit(1)

def gen_sshkey():
    key = RSA.generate(2048)
    priv_key_file = '/home/ubuntu/.ssh/id_rsa'
    pub_key_file = '/home/ubuntu/.ssh/id_rsa.pub'
    uid = pwd.getpwnam("ubuntu").pw_uid
    if os.path.exists(priv_key_file):
        return
    with open(priv_key_file, 'w') as content_file:
        os.chmod(priv_key_file, stat.S_IREAD)
        os.chown(priv_key_file, uid, -1)
        content_file.write(key.exportKey('PEM').decode('utf-8'))
    pubkey = key.publickey()
    with open(pub_key_file, 'w') as content_file:
        os.chown(pub_key_file, uid, -1)
        content_file.write(pubkey.exportKey('OpenSSH').decode('utf-8'))
