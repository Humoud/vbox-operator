import re
import subprocess
from commands_dict import completer_dict
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style, style
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession, print_formatted_text

# from: https://www.colourlovers.com/palette/1718713/Monokai
# and:  https://www.color-hex.com/color-palette/59231
cli_style = Style.from_dict({
    # User's input.
    '':   '#66D9EF', # cyanish
    # Prompt
    'vm': '#F92672', # pinkish
    'gt': '#A6E22E', # greenish
    'output1': '#FD971F', # orangish
    'output2': '#AE81FF' # purplish
})

pybox_completer = NestedCompleter.from_nested_dict(completer_dict)
# current vm
curr_vm = None
# all vms
vms = 0
# running vms
r_vms = 0

##########################################
# HELPERS


def command_runner(args):
    args = args.split(' ')
    res = subprocess.run(
            args, stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
    return res


def init_vms_data():
    global completer_dict
    global pybox_completer
    global vms
    global r_vms
    vm_names = []
    # all vms
    result = command_runner('vboxmanage list vms')
    for l in result.split('\n'):
        vm_name = re.search(r'"(.*)"', l)
        vm_uuid = re.search(r'{(.*)}$', l)
        if vm_name and vm_uuid:
            vms += 1
            vm_names.append(vm_name.group(1))
    # running vms
    result = command_runner('vboxmanage list runningvms')
    for l in result.split('\n'):
        vm_name = re.search(r'"(.*)"', l)
        vm_uuid = re.search(r'{(.*)}$', l)
        if vm_name and vm_uuid:
            r_vms += 1
    # update auto complete
    if vm_names:
        c = completer_dict.copy()
        for v in vm_names:
            if c['set']['vm'] == None:
                c['set']['vm']={v: None}
            else:
                c['set']['vm'][v] = None
        pybox_completer = NestedCompleter.from_nested_dict(c)


def print_vm_list(result):
    global cli_style
    vm_counter = 0
    msg = [
        ('class:output2', '-'*88+'\n'),
        ('class:output1', '#  '),
        ('class:output2', '|'),
        ('class:output1', f' VM Name { " " :<21} '),
        ('class:output2', '|'),
        ('class:output1', ' VM UUID\n'),
    ]
    for l in result.split('\n'):
        vm_name = re.search(r'"(.*)"', l)
        vm_uuid = re.search(r'{(.*)}$', l)
        if vm_name and vm_uuid:
            vm_counter += 1
            msg.append(('class:output2', '-'*88+'\n'))
            msg.append(('class:output1', f'{vm_counter:<3}'))
            msg.append(('class:output2', '|'))
            msg.append(('class:output1', f' {vm_name.group(1):<30}'))
            msg.append(('class:output2', '|'))
            msg.append(('class:output1', f' {vm_uuid.group(1)}\n'))
            
    print_formatted_text(FormattedText(msg), style=cli_style)


def print_snapshot_list(result):
    global cli_style
    snapshot_counter = 0
    msg = [
        ('class:output2', '-'*88+'\n'),
        ('class:output1', '#  '),
        ('class:output2', '|'),
        ('class:output1', f' Snapshot Name { " " :<15} '),
        ('class:output2', '|'),
        ('class:output1', ' VM UUID\n'),
    ]
    for l in result.split('\n'):
        snapshot_name = re.search(r'Name: (.*) \(', l)
        snapshot_uuid = re.search(r'UUID: (.*)\)', l)
        if snapshot_name and snapshot_uuid:
            snapshot_counter += 1
            msg.append(('class:output2', '-'*88+'\n'))
            msg.append(('class:output1', f'{snapshot_counter:<3}'))
            msg.append(('class:output2', '|'))
            msg.append(('class:output1', f' {snapshot_name.group(1):<30}'))
            msg.append(('class:output2', '|'))
            msg.append(('class:output1', f' {snapshot_uuid.group(1)}\n'))
    print_formatted_text(FormattedText(msg), style=cli_style)

#########################################
# VBOX WRAPPERS

def list_vms(cmd):
    # reset list
    vm_name = []
    # update/create list
    result = None
    try:
        if cmd[2] == 'running':
            result = command_runner('vboxmanage list runningvms')
        else:
            print("Error, unknown command")
            return
    except IndexError:
        result = command_runner('vboxmanage list vms')
    print_vm_list(result)
    

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
        print_snapshot_list(result)
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


def acpipower_vm(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} acpipowerbutton')
        print(result)
        print('ACPI shutdown signal sent to VM.\nPlease check VM status after a minute or two.')
    else:
        print('Error, please select a VM via the "set vm" command.')


def reset_vm(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} reset')
        print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')


def pause_vm(cmd_arr, vm):
    if vm:
        result = command_runner(f'vboxmanage controlvm {vm} pause')
        print(result)
    else:
        print('Error, please select a VM via the "set vm" command.')


def help_menu():
    global curr_vm
    global cli_style
    if curr_vm:
        msg = [
            ( 'class:output1','\n  show state\n'),
            ( 'class:output2','    Show the state of the currently selected VM.\n'),
            ( 'class:output1','  show snapshots\n'),
            ( 'class:output2','    Show the list of snapshots for the currently selected VM.\n'),
            ( 'class:output1','  restore snapshot SNAPSHOT_NAME/SNAPSHOT_UUID\n'),
            ( 'class:output2','    Revert the state of the currently select VM to the specified snapshot.\n'),
            ( 'class:output1','  start vm\n'),
            ( 'class:output2','    Start the currently selected VM.\n'),
            ( 'class:output1','  reset vm\n'),
            ( 'class:output2','    Restart the currently selected VM.\n'),
            ( 'class:output1','  acpipowerbutton vm\n'),
            ( 'class:output2','    Send ACPI shutdown signal (shutdown button) to the currently selected VM.\n'),
            ( 'class:output1','  poweroff vm\n'),
            ( 'class:output2','    Force shutdown (like pulling the power plug) the currently selected VM.\n'),
            ( 'class:output1','  back\n'),
            ( 'class:output2','    Go back to main menu.\n'),
            ( 'class:output1','  exit\n'),
            ( 'class:output2','    Exit program.\n')
        ]
        print_formatted_text(FormattedText(msg), style=cli_style)
    else:
        msg = [
            ('class:output1','\n  list vms\n'),
            ('class:output2','    List all VMs (shortcut: ls).\n'),
            ('class:output1','  list vms running\n'),
            ('class:output2','    List all running VMs (shortcut: ls vms running).\n'),
            ('class:output1','  set vm VM_NAME/VM_UUID\n'),
            ('class:output2','    Select a VM to operate on.\n'),
            ('class:output1','  exit\n'),
            ( 'class:output2','    Exit program.\n')
        ]
        print_formatted_text(FormattedText(msg), style=cli_style)


def handle_cmd(cmd):
    global curr_vm
    try:
        if (cmd[0] == 'list' and cmd[1] == 'vms') or (cmd[0] == 'ls'):
            list_vms(cmd)
        elif cmd[0] == 'set' and cmd[1] == 'vm':
            set_vm(cmd[2])
        elif cmd[0] == 'start':
            start_vm(cmd, curr_vm)
        elif cmd[0] == 'show':
            # checking for 'status' to be more lenient
            if cmd[1] == 'state' or cmd[1] == 'status':
                state_vm(cmd, curr_vm)
            if cmd[1] == 'snapshots':
                list_snapshots(cmd, curr_vm)
        elif cmd[0] == 'restore' and cmd[1] == 'snapshot':
            restore_vm(cmd, curr_vm)
        elif cmd[0] == 'poweroff':
            poweroff_vm(cmd, curr_vm)
        elif cmd[0] == 'acpipowerbutton':
            acpipower_vm(cmd, curr_vm)
        elif cmd[0] == 'pause':
            pause_vm(cmd, curr_vm)
        elif cmd[0] == 'reset':
            reset_vm(cmd, curr_vm)
        elif cmd[0] == 'help' or cmd[0] == 'h':
            help_menu()
        elif cmd[0] == 'back':
            curr_vm = None
        elif cmd[0] == 'exit':
            quit()
    except IndexError:
        print('Error, command not recognized.\nTry running "help"')


def banner():
    global cli_style
    global r_vms
    global vms
    msg = [
        ('class:vm', 'VBox Operator '),
        ('class:gt', 'v0.1\n'),
        ('class:output2', f'Available VMs: {vms}\n'),
        ('class:output1', f'Running VMs: {r_vms}')
    ]
    print_formatted_text(FormattedText(msg), style=cli_style)


if __name__ == "__main__":
    banner()
    # Create prompt object.
    session = PromptSession()
    init_vms_data()
    while True:
        cli = [
            ('class:gt',    ' > ')
        ]
        if curr_vm:
            cli.insert(0, ('class:vm', curr_vm) )
        
        cmd = session.prompt(cli, completer=pybox_completer, style=cli_style)
        cmd = cmd.split(' ')
        handle_cmd(cmd)


    