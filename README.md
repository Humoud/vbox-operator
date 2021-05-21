# VBox Operator
#### v0.0.4
An interactive command line interface for VirtualBox.

Supported Features:
1. Commands and VM name auto-completion.
2. Start, stop, and pause VMs.
3. Restore snapshots.
4. Copy files and directories to guest VMs.

### Usage

[![asciicast](https://asciinema.org/a/xmHAkuMqCxhUsoip8axSkSRaX.svg)](https://asciinema.org/a/xmHAkuMqCxhUsoip8axSkSRaX)

### Installation

``` bash
> python3 -m pip install vbox-operator
> vbox-operator
```

### Library Usage

Example: Listing running VMs and getting the status of each one.

``` python
from vbox_operator.operations import *

vm_list = list_vms() # returns a dict of lists
for vm in vm_list["running"]:
    vm_name = vm["name"]
    print(f'Running: {vm_name}')
    vm_state = state_vm(vm["uuid"])
    print(f'  > {vm_state}')
```

Below is a list of all implemented methods, I did my best to make the naming as self explanatory as possible:

```python 
# returns dict of lists: 
# {"all": [], "running": []}
# while each list is a list of dicts: {"name": "VM NAME", "uuid": "VM UUID}
list_vms()

### For all methods below which take param "vm",
# you may pass the VM name or UUID as a VM identifier.
# However, it is best to provide the VM UUID, as it may prevent some issues.
start_vm_headless(vm)
start_vm(vm)
state_vm(vm)
# Pull power plug on the VM
poweroff_vm(vm)
# Send ACPI shutdown signal to VM (power button)
acpipower_vm(vm)
# restart VM
reset_vm(vm)
pause_vm(vm)

# Returns a list of dicts: [{"name": "SNAPSHOT NAME", "uuid": "SNAPSHOT UUID},]
list_snapshots(vm)

# param snapshot is expected to be a snapshot identifier,
# it is best to pass the snapshot UUID instead of the VM name.
restore_vm(vm, snapshot)

### The methods below expect the username and password of the guest VM,
# and the direction of the operations is Host to Guest.
mkdir_vm(username, password, vm, directory)
copyfile_vm(username, password, vm, src_file, dst)
copydir_vm(username, password, vm, src_dir, dst)
```

### Support
This tool was developed and tested on ubuntu 18.04 with the following installed:
1. VirtualBox v6.1.x
2. Python >= 3.6

I ran a quick test on MacOS and it worked.

By theory, it should work on Windows as well if VirtualBox's vboxmanage binary is available in your PATH. 

Note that for certain features like copying files and dirs, the guest VM must have guest additions installed.


### Current Limitations
The command line interface does not support VM and snapshot names which contain spaces, however, you can use the VM UUID or snapshot UUID instead.
