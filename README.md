# VBox Operator
#### v0.0.3
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

### Support
This tool was developed and tested on ubuntu 18.04 with the following installed:
1. VirtualBox v6.1.x
2. Python >= 3.6

I ran a quick test on MacOS and it worked.

By theory, it should work on Windows as well if VirtualBox's vboxmanage binary is available in your PATH. 

Note that for certain features like copying files and dirs, the guest VM must have guest additions installed.
