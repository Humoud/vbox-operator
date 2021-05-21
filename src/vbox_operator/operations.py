import re
import subprocess
from vbox_operator.menu import help_menu
from vbox_operator.commands_dict import completer_dict

##########################################
# HELPERS


def command_runner(args):
    args = args.split(' ')
    res = subprocess.run(
            args, stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
    return res


def get_vm_list(result):
    vm_list = []
    for l in result.split('\n'):
        vm_name = re.search(r'"(.*)"', l)
        vm_uuid = re.search(r'{(.*)}$', l)
        if vm_name and vm_uuid:
            vm_list.append({
                "name": vm_name.group(1),
                "uuid": vm_uuid.group(1)
            })
    return vm_list


def get_snapshot_list(result):
    snapshot_list = []
    for l in result.split('\n'):
        snapshot_name = re.search(r'Name: (.*) \(', l)
        snapshot_uuid = re.search(r'UUID: (.*)\)', l)
        if snapshot_name and snapshot_uuid:
            snapshot_list.append({
                'name': snapshot_name.group(1),
                'uuid':snapshot_uuid.group(1)
            })
    return snapshot_list

#########################################
# VBOX WRAPPERS

def list_vms():
    all_vms = get_vm_list(command_runner('vboxmanage list vms'))
    running_vms = get_vm_list(command_runner('vboxmanage list runningvms'))
    return {'all': all_vms, 'running': running_vms}


def start_vm_headless(vm):
    if vm:
        result = command_runner(f'vboxmanage startvm {vm} --type headless')
        return result
    else:
        return None


def start_vm(vm):
    if vm:
        result = command_runner(f'vboxmanage startvm {vm}')
        return result
    else:
        return None


def poweroff_vm(vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} poweroff')
        return result
    else:
        return None


def state_vm(vm):
    if vm:
        try:
            result = command_runner(f'vboxmanage showvminfo {vm} --details')
            state = re.search(r'State:\s*(.*)',result).group(1)
            return state
        except AttributeError:
            return None
    else:
        return None


def list_snapshots(vm):
    if vm:
        result = command_runner(f'vboxmanage snapshot {vm} list')
        snapshot_list = get_snapshot_list(result)
        return snapshot_list
    else:
        return None


def restore_vm(vm, snapshot):
    if vm:
        result = command_runner(f'vboxmanage snapshot {vm} restore {snapshot}')
        return result
    else:
        return None


def acpipower_vm(vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} acpipowerbutton')
        return result
    else:
        return None


def reset_vm(vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} reset')
        return result
    else:
        return None


def pause_vm(vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} pause')
        return result
    else:
        return None


def mkdir_vm(username, password, vm, directory):
    if vm:
        result = command_runner(
            f'vboxmanage guestcontrol {vm} mkdir '
            f'--username {username} --password {password} '
            f'--parents {directory}'
        )
        return result
    else:
        return None


def copyfile_vm(username, password, vm, src_file, dst):
    if vm:
        result = command_runner(
            f'vboxmanage guestcontrol {vm} copyto '
            f'--username {username} --password {password} '
            f'{src_file} --target-directory {dst}'
        )
    else:
        return None

def copydir_vm(username, password, vm, src_dir, dst):
    if vm:
        # create dir on guest vm
        mkdir_vm(username, password, vm, dst)
        # copy dir
        result = command_runner(
            f'vboxmanage guestcontrol {vm} copyto '
            f'--username {username} --password {password} '
            f'{src_dir} -R --target-directory {dst}'
        )
        return result
    else:
        return None