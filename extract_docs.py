#!/usr/bin/python2

import imp

filenames = [
	"collect",
	"view",
	"bins",
	"calculate",
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
python2 -V

- install tshark via packet manager
sudo apt install tshark
select enable non-sudo capture, then add privledge to current user with
sudo usermod -aG wireshark $USER

- install matplotlib via packet manager
sudo apt-get install python-matplotlib

- install python pip
sudo apt install python-pip

- use pip to install python requirements
pip2 install -r requirements
"""

def main():
	docs = [get_doc(f) for f in filenames]
	usage_instructions = "\n".join(docs)
	outputs = [install_title, install_instructions, usage_title, usage_instructions]
	output = "\n" + "\n".join(outputs) + "\n"
	with open("docs/README.md", "w") as f:
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
