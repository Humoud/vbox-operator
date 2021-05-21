# VBox Operator
An interactive command line interface for VirtualBox.

Supported Features:
1. Commands and VM name auto-completion.
2. Start, stop, and pause VMs.
3. Restore snapshots.
4. Copy files and directories to guest VMs.

[![asciicast](https://asciinema.org/a/eL4W80xzruLS1nVz2B359xfoo.svg)](https://asciinema.org/a/eL4W80xzruLS1nVz2B359xfoo)

### Installation

``` bash
python3 -m pip install vbox-operator
vbox-operator
```

### Support
This tool was developed and tested on ubuntu 18.04. By theory, it should work on Windows and MacOs if VirtualBox's vboxmanage binary is available in your PATH. For certain features like copying files and dirs, the guest VM must have guest additions installed.
