# VBox Operator
An interactive command line interface for virtual box.

Supported Features:
1. Start, stop, and pause VMs.
2. Restore snapshots.
3. Copy files and directories to guest VMs.

[![asciicast](https://asciinema.org/a/eL4W80xzruLS1nVz2B359xfoo.svg)](https://asciinema.org/a/eL4W80xzruLS1nVz2B359xfoo)

### Installation
Note: this tool was developed and tested on ubuntu 18.04. For certain features like copying files and dirs, the guest VM must have guest additions installed.

``` bash
python3 -m pip install -r requirements.txt
python3 vboxoperator.py
```
