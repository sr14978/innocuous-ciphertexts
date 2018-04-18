#!/usr/bin/python2

import imp

filenames = [
	"collect",
	"visit_http",
	"view",
	"bins",
	"calculate",
	"visualise_bins",
	"find_threshold",
	"measure",
	"run_emulator",
	"graph",
	"test_emulator"
]

install_title = "# INSTALLATION"
usage_title = "# USAGE"

install_instructions = """
- ensure python2 is installed
```bash
python2 -V
```

- install tshark via packet manager
```bash
sudo apt install tshark
```
select enable non-sudo capture, then add privledge to current user with
```bash
sudo usermod -aG wireshark $USER
```
(will have to log back on for it to take effect)

- install matplotlib via packet manager
```bash
sudo apt-get install python-matplotlib
```

- install python pip
```bash
sudo apt install python-pip
```

- use pip to install python requirements
```bash
pip2 install -r requirements
```
"""

def main():
	docs = [get_doc(f) for f in filenames]
	usage_instructions = "\n".join(docs)
	outputs = [install_title, install_instructions, usage_title, usage_instructions]
	output = "\n" + "\n".join(outputs) + "\n"
	with open("README.md", "w") as f:
		f.write(output)

def get_doc(filename):
	with open(filename + ".py", "r") as f:
		return imp.load_module(
			filename,
			f,
			filename+".py",
			("py", "r", imp.PY_SOURCE)
		).__doc__

if __name__ == "__main__":
	main()
