import re
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter

completer_dict = {
    'back': None,
    'list': {
        'vms': {'running': None}
    },
    'set':{
        'vm': None
    },
    'restore': {
        'snapshot': None
    },
    'show': {
        'state': None,
        'snapshots': None
    },
    'start': {
        'vm': {'headless': None}
    },
    'poweroff': {
        'vm': None
    }
}
pybox_completer = NestedCompleter.from_nested_dict(completer_dict)

curr_vm = None
vm_names = []

def command_runner(args):
    args = args.split(' ')
    res = subprocess.run(
            args, stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
    return res

def list_vms(cmd):
    global vm_names
    global completer_dict
    global pybox_completer
    # reset list
    vm_name = []
    # update/create list
    if len(cmd) > 2:
        result = command_runner('vboxmanage list runningvms')
    else:
        result = command_runner('vboxmanage list vms')
    vm_counter = 0
    print('-'*88)
    print(f'#  | VM Name { " " :<21} | VM UUID')
    for l in result.split('\n'):
        vm_name = re.search(r'"(.*)"', l)
        vm_uuid = re.search(r'{(.*)}$', l)
        if vm_name and vm_uuid:
            vm_counter += 1
            print('-'*88)
            print(f'{vm_counter:<3}| {vm_name.group(1):<30}| {vm_uuid.group(1)}')
            vm_names.append(vm_name.group(1))
    if vm_names:
        # add vm names to auto complete
        c = completer_dict.copy()
        for v in vm_names:
            if c['set']['vm'] == None:
                c['set']['vm']={v: None}
            else:
                c['set']['vm'][v] = None
        pybox_completer = NestedCompleter.from_nested_dict(c)

def set_vm(vm):
    global curr_vm
    if vm:
        curr_vm = vm
    else:
        print("Error, please provide a VM UUID or name.")

def start_vm(cmd_arr, vm):
    if vm:
        if len(cmd) > 2:
            if cmd[2] == 'headless':
                result = command_runner(f'vboxmanage startvm {vm} --type headless')
                print(result)
            else:
                print('Error, unknown command')
        else:
            result = command_runner(f'vboxmanage startvm {vm}')
            print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')

def poweroff_vm(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} poweroff')
        print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')


def state_vm(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage showvminfo {vm} --details')
        state = re.search(r'State:\s*(.*)',result).group(1)
        print(state)
    else:
        print('Error, please select a VM via the "set vm" command.')


def list_snapshots(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage snapshot {vm} list')
        print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')


def restore_vm(cmd_arr, vm):
    if vm:
        if len(cmd_arr) >= 2:
            snapshot = cmd_arr[2]
            result = command_runner(f'vboxmanage snapshot {vm} restore {snapshot}')
            print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')


# Create prompt object.
session = PromptSession()
while True:
    p = ' > '
    if curr_vm:
        p = f' {curr_vm} > '
    cmd = session.prompt(p, completer=pybox_completer)
    cmd = cmd.split(' ')
    if cmd[0] == 'list':
        if cmd[1] == 'vms':
            list_vms(cmd)
    elif cmd[0] == 'set':
        if cmd[1] == 'vm':
            set_vm(cmd[2])
    elif cmd[0] == 'start':
        start_vm(cmd, curr_vm)
    elif cmd[0] == 'poweroff':
        poweroff_vm(cmd, curr_vm)
    elif cmd[0] == 'show':
        if cmd[1] == 'state':
            state_vm(cmd, curr_vm)
        if cmd[1] == 'snapshots':
            list_snapshots(cmd, curr_vm)
    elif cmd[0] == 'restore':
        if cmd[1] == 'snapshot':
            restore_vm(cmd, curr_vm)
    elif cmd[0] == 'back':
        curr_vm = None
    elif cmd[0] == 'exit':
        quit()


    