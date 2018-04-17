
# INSTALLATION

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

# USAGE

This program allows you to collect some url paths from unencrypted http requests in the following way
./collect.py --output <output_filepath> --size <number_of_urls>
eg ./collect.py --output 100/fakes/1 --size 100

There are already examples stored in

- 100/fakes/
- 100/normals/
- 100/emulated/

and a reference list to test against at
- 100/reference_urls


This program can be used to view data such as urls and distrobution historgram bins as follows
./view.py <filepath>
eg ./view.py 100/reference_urls


A distrobution historgram of the urls can be computed with this bin program. You can choose one of the following methods:
  - CHARACTER_DISTROBUTION:'char'
  - SLASHES_FREQUENCY:'slash'
  - INTER_SLASH_DIST:'length'
  - FIRST_LETTER:'first'
  - RANDOM_LETTER:'rand'

./bins.py --in 100/reference_urls --out 100/reference_<method>_bins --mode <method>
eg ./bins.py --in 100/reference_urls --out 100/reference_char_bins --mode char


You can calculate the distance between given urls and a reference distrobution with this program.
./calculate.py <url_test_file> <reference_bins>
eg ./calculate.py 100/fakes/1 100/reference_char_bins


This program can calculate a decision threshold to differentiate the normal and fake distrobutions.
./find_threshold.py --mode <binning_method>
eg ./find_threshold.py --mode charq


You can use the measure program to decide if urls are fake or normal. Leaving off the index will collect new urls using the collect program
./measure.py --size <number_of_urls> --folder <folder> --index <#> --mode <binning_method>
eg ./measure.py --size 100 --folder fakes --index 1 --mode char


You can use the emulator program to produce url messages that emulate the reference distrobution
./run_emulator.py --out <output_filepath> --mode <binning_method>
eg ./run_emulator.py --out 100/emulated/char/1 --mode char


This program can display the relation of normal, fake and emulated distrobutions to a reference distrobution.
./graph.py --mode <binning_method>
eg ./graph.py --mode char


You can test that the emulated ciphertexts are like the reference distrobution  and is that the encoding invertable using this program.
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char

