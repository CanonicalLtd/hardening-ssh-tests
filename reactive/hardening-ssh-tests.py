from charms.reactive import (
  is_state, set_state,
  when, when_not,
  hookenv, hook,
)

@when('ruby.available')
def setup_tests():
    clone()
    bundle('install')


def clone():
    cmd =  "git clone {} {}".format('https://github.com/hardening-io/tests-ssh-hardening.git', config['app-path'])
    res = check_call(cmd, shell=True)
    if res != 0:
      status_set('error', 'has a problem with git, try `resolved --retry')
      sys.exit(1)