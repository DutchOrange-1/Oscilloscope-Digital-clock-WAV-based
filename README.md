# Oscilloscope-Digital-clock-WAV-based
This is a Oscilloscope Digital clock, which is powered using WAV files, and a PC or PI. Ran using Python. 

# Usage
Make sure to put the ``clock.py`` file and folder of wav files in the same location, and run the script. 

# Generation of clock
To save on space, a short wav file has been generated for each symbol, and all the device must do is play that file on repeat.
This reduces the 8 GB down to about 25 MB, which is done as the Pi Zero W I am using does not have the processing power to continuously generate the clock face. 

The current Version makes use of a 7-segment type display, each segment is plotted separately, scaled and shifted using the ``seven_seg_gen.py`` file. 




