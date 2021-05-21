from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText


def help_menu(curr_vm, cli_style):
    # vm selected menu
    if curr_vm:
        msg = [
            ( 'class:output1','\n  show state\n'),
            ( 'class:output2','    Show the state of the currently selected VM.\n'),
            ( 'class:output1','  show snapshots\n'),
            ( 'class:output2','    Show the list of snapshots for the currently selected VM.\n'),
            ( 'class:output1','  restore snapshot SNAPSHOT_NAME/SNAPSHOT_UUID\n'),
            ( 'class:output2','    Revert the state of the currently select VM to the specified snapshot.\n'),
            ( 'class:output1','  copyfile HOST_FILE_PATH VM_FILE_PATH \n'),
            ( 'class:output2','    Copy a file from the host to the guest VM (creds required).\n'),
            ( 'class:output1','  copydir HOST_DIR_PATH/ VM_FILE_PATH \n'),
            ( 'class:output2','    Copy a directory recursively from the host to the guest VM (creds required).\n'),
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
    # no vm selected menu
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