import os
import sys
import json
import yaml

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.plugins.callback import CallbackBase
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        if u'stdout' in result._result:
            print result._result[u'stdout']


variable_manager = VariableManager()
loader = DataLoader()

inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list=['localhost'])
playbook_path = './echo.yml'

if not os.path.exists(playbook_path):
    print '[INFO] The playbook does not exist'
    sys.exit()

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='local', module_path=None, forks=100, remote_user=None, private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=False, become_method=None, become_user='root', verbosity=None, check=False)

passwords = {}

stdout_callback = ResultCallback()

with open(playbook_path) as stream:
	play_book, = yaml.load(stream)
	play = Play().load(play_book, variable_manager=variable_manager, loader=loader)

tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              options=options,
              passwords=passwords,
              #stdout_callback=stdout_callback,
          )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()
