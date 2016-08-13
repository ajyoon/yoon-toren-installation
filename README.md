# Yoon/Toren Installation 5/10/2016

Two programs used as part of an installation built by Cat Toren and Andrew
Yoon which was up on May 10, 2016 at Purchase College.

#### About the Original Project

A microphone was set up in front of a printed booklet of algorithmically
built text. Viewers of the installation were encouraged to read from the
text into the microphone. A series of digital sine wave oscillators
spontaneously played tones while audio captured from the microphone was
remembered and recalled over time.

The seed text which formed the basis of the algorithmically built text was
written by Cat Toren while Andrew Yoon wrote the programs which transformed
the text and which processed and generated the sound.

You can listen to a recording of the installation online
[here](https://www.youtube.com/watch?v=vBFPbpDtKeI), and you can
view an example of the algorithmically generated text
[here] (example/example_book.pdf).

Cat Toren is a jazz pianist, improviser, and composer; to hear her other works
or get in touch, you can find her online [here](http://cat-toren.com/).

-------------------------------------------------------------------------------

## Setup

Running the programs in this project requires Python 3, if you do not have it
installed you can do so [here](https://www.python.org/).

To get started, download this repository onto your local machine.
Use your system's command line to navigate to the project location
and install its dependencies using pip.

    cd path/to/yoon-toren-installation
    pip install -r requirements.txt

## Running

To generate the algorithmic poem booklet, run `python build_book.py`.
This will generate a PDF document, place it in `bookmaker/output`,
and open the file.

To run the audio processing program, run `python run_electronics.py`.

### Troubleshooting

###### run_electronics.py
Depending on the audio environment of your system, you may need to modify the
I/O device indices used by the program. You can temporarily set these with the
`-i your_input_device_index` and `-o your_output_device_index` arguments.
To change the default indices used, open `electronics/config.py`
and edit `DEFAULT_INPUT_DEVICE_INDEX` and `DEFAULT_OUTPUT_DEVICE_INDEX`.

To view a list of available devices and their indices,
run the program with the debug flag `-d` or `--debug`
ie. `python run_electronics.py --debug`.

### Things that may not work yet

This project was originally hacked together in May 2016, and contained lots
of poor decisions. Extensive work is currently underway refactoring and
rewriting the code, but in the meantime please forgive any bugs or ugliness.

The `run_electronics.py` script has *only* been tested so far on Ubuntu
using PortAudio. Modifications may need to be made to get it working on
your system. See "Troubleshooting" above for more details.

#### TODO:

* Continue improving docstrings and code legibility
* Continue refactoring to fix the various quick hacks used throughout
* Consider possibly splitting the two sub-projects into separate repos
* Better explanation for how to configure the audio environment
* Test audio configurations on other OS's and audio drivers.
* Implement automatic level adjustments to prevent clipping when the output
    becomes too loud.
