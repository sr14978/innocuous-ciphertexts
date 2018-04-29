
# INSTALLATION

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
- (for web crawler only) install geckodriver by downloading archive, extracting the executable and putting it on your PATH
REPO: https://github.com/mozilla/geckodriver/releases
```bash
sudo mv geckodriver /usr/bin/
```

- (for web crawler only) install selenium web automation framework
```bash
pip install selenium --user
```

- install python pip
```bash
sudo apt install python-pip
```

- use pip to install python requirements
```bash
pip2 install -r requirements
```

# USAGE

This program allows you to collect some url paths from unencrypted http requests in the following way
```bash
./collect.py --output <output_filepath> --size <number_of_urls>
eg ./collect.py --output 1000/fakes/1 --size 1000
```

There are already examples stored in

- 1000/fakes/
- 1000/normals/
- 1000/emulated/

and a reference list to test against at
- 1000/censor/reference_urls


This simple web crawler program will follow links on webpages to create normal looking traffic.
```bash
./visit_http
```


This program can be used to view data such as urls and distrobution historgram bins as follows
```bash
./view.py <filepath>
eg ./view.py 1000/censor/reference_urls
```


A distrobution historgram of the urls can be computed with this bin program. You can choose one of the following methods:
  - PATTERN_DISTROBUTION:'pattern',
  - CHARACTER_DISTROBUTION:'char'
  - SLASHES_FREQUENCY:'slash'
  - INTER_SLASH_DIST:'dist',
  - FIRST_LETTER:'first'
  - RANDOM_LETTER:'rand'
  - URL_LENGTH:'length'

```bash
./bins.py --in 1000/censor/reference_urls --out 1000/censor/reference_<method>_bins --mode <method>
eg ./bins.py --in 1000/censor/reference_urls --out 1000/censor/reference_char_bins --mode char
```


You can calculate the distance between given urls and a reference distrobution with this program.
```bash
./calculate.py <url_test_file> <reference_bins>
eg ./calculate.py 1000/fakes/1 1000/censor/reference_char_bins
```


You can use this program to compare visually how the url distrobutions compare.
```bash
./visualise_bins.py -m <binning_mode>
eg ./visualise_bins.py -m char
```


This program can calculate a decision threshold to differentiate the normal and fake distrobutions.
```bash
./find_threshold.py --mode <binning_method>
eg ./find_threshold.py --mode char
```


You can use the measure program to decide if urls are fake or normal. Leaving off the index will collect new urls using the collect program
```bash
./measure.py --size <number_of_urls> --folder <folder> --index <#> --mode <binning_method>
eg ./measure.py --size 1000 --folder fakes --index 1 --mode char
```


You can use the emulator program to produce url messages that emulate the adversary reference distrobution
```bash
./run_emulator.py --out <output_filepath> --mode <binning_method>
eg ./run_emulator.py --out 1000/emulated/char/1 --mode char
```


This program can display the relation of normal, fake and emulated distrobutions to a reference distrobution.
```bash
./graph.py --mode <binning_method>
eg ./graph.py --mode char
```


You can test that the emulated ciphertexts are like the adversary reference distrobution  and is that the encoding invertable using this program.
```bash
./test_emulator.py --mode <binning_method>
eg ./test_emulator.py --mode char
```


Program to run all functions with default paths. -c enables collecting all new packets. -g displays the graphs as it goes along. -e enables emulation calculations.
```bash
./run_all.py -c -g -e
```

