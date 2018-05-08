# PitchGenerator

## Dependencies
On Mac OS X

### PyAudio (Python 3)
```
import pyaudio
```
### wave (Python 3)
```
import wave
```
### scipy
```
pip install scipy
import scipy
```
### numpy
```
pip install numpy
import numpy
``` 
### Jupyter Notebook
```
pip install jupyter
jupyter notebook
```
### Librosa
```
conda install -c conda-forge librosa
import librosa
```
### Pretty MIDI
```
pip install pretty_midi
import pretty_midi
```
### Pydub
```
pip install pydub
import pydub
```
### MIDIUtil
```
pip install MIDIUtil
import midiutil
```
### Melodia (Pitch Recognition)
* Install Vamp
```
pip install vamp
import vamp
```
* Download Plugin from <https://www.upf.edu/web/mtg/melodia>
* Unzip __MTG-MELODIA 1.0 (OSX universal).zip__
* Copy all files in __MTG-MELODIA 1.0 (OSX universal).zip__ to: __/Library/Audio/Plug-Ins/Vamp__
### Timidity (MIDI to wav conversion)
```
brew install timidity
```
### FluidR3 GM Bank (Timidity Soundfont)
* Download FluidR3 GM Bank Soundfont2 from <https://archlinux.pkgs.org/rolling/archlinux-community-x86_64/soundfont-fluid-3.1-1-any.pkg.tar.xz.html>
* Unzip __soundfont-fluid-3.1-1-any.pkg.tar.xz__
```
tar xvfJ soundfont-fuid-3.1.1-any.pkg.tar.xz
```
* Find __/usr/share/soundfonts/FluidR3_GM.sf2__ and put to whatever path
* Open Timidity config file
```
vim /usr/local/Cellar/timidity/2.14.0/share/timidity/timidity.cfg
```
* Add line to top of the cfg file
```
soundfont /path/to/FluidR3_GM.sf2
```
* Save 
