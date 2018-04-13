
# INSTALLATION

- ensure python2 is installed
python2 -V

- install tshark via packet manager
sudo apt install tshark

- install matplotlib via packet manager
sudo apt-get install python-matplotlib

- use pip to install python requirements
pip2 install -r requirements

# USAGE

- You can collect some urls using the collect program
./collect.py --output <output_filepath> --size <number_of_urls>
eg ./collect.py --output 100/fakes/1 --size 100

  There are already examples stored in

  - 100/fakes/
  - 100/normals/
  - 100/emulated/
  
  and a reference list to test against at
  - 100/reference_urls
  
- These can be viewed using the print program
./print.py <filepath>
eg ./print.py 100/reference_urls

- A distrobution historgram can be computed with the bin program. You can choose one of the following methods:
  - CHARACTER_DISTROBUTION:'char'
  - SLASHES_FREQUENCY:'slash'
  - INTER_SLASH_DIST:'length'
  - FIRST_LETTER:'first'
  - RANDOM_LETTER:'rand'

  ./bins.py --input 100/reference_urls \
	--output 100/reference_<method>_bins \
	--mode <method>
  eg ./bins.py --input 100/reference_urls \
	--output 100/reference_char_bins \
	--mode char
	
- You can calculate the distance between given urls and a reference distrobution with the calculate program
./calculate.py <url_test_file> <reference_bins>
eg ./calculate.py 100/fake/1 100/reference_char_bins

- A threshold can be found to differentiate the normal and fake distrobutions using the find threshold program
./find_threshold.py --mode <binning_method>
eg ./find_threshold.py --mode char

- You can use the measure program to decide if urls are fake or normal. Leaving off the index will collect new urls using the collect program
./measure.py --size <number_of_urls> --folder <folder> --index <#> --mode <binning_method>
eg ./measure.py --size 100 --folder fakes --index 1 --mode char

- You can use the emulator program to produce url messages that emulate the reference distrobution
./emulate.py --output <output_filepath> --mode <binning_method>
./emulate.py --output 100/emulated/char/1 --mode char

- You can also see how emulation is doing with the graph program
./graph.py --mode <binning_method>
./graph.py --mode char

- You can test the emulation using the test emulator program
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char

