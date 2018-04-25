import librosa
import vamp
import argparse
import os
import numpy as np
from midiutil import MIDIFile
from scipy.signal import medfilt
import jams
import __init__


def hz2midi(hz):
    # convert from Hz to midi note
    hz_nonneg = hz.copy()
    idx = hz_nonneg <= 0
    hz_nonneg[idx] = 1
    midi = 69 + 12 * np.log2(hz_nonneg / 440.)
    midi[idx] = 0

    # round
    midi = np.round(midi)

    return midi


def midi_to_notes(midi, fs, hop, smooth, minduration):
    # smooth midi pitch sequence first
    if smooth > 0:
        filter_duration = smooth  # in seconds
        filter_size = int(filter_duration * fs / float(hop))
        if filter_size % 2 == 0:
            filter_size += 1
        midi_filt = medfilt(midi, filter_size)
    else:
        midi_filt = midi
    # print(len(midi),len(midi_filt))

    notes = []
    p_prev = None
    duration = 0
    onset = 0
    for n, p in enumerate(midi_filt):
        if p == p_prev:
            duration += 1
        else:
            # treat 0 as silence
            if p_prev is not None and p_prev > 0:
                # add note
                duration_sec = duration * hop / float(fs)
                # only add notes that are long enough
                if duration_sec >= minduration:
                    onset_sec = onset * hop / float(fs)
                    notes.append((onset_sec, duration_sec, p_prev))

            # start new note
            onset = n
            duration = 1
            p_prev = p

    # add last note
    if p_prev > 0:
        # add note
        duration_sec = duration * hop / float(fs)
        onset_sec = onset * hop / float(fs)
        notes.append((onset_sec, duration_sec, p_prev))

    return notes


def save_midi(outfile, notes, tempo):

    track = 0
    time = 0
    midifile = MIDIFile(1)

    # Add track name and tempo.
    midifile.addTrackName(track, time, "MIDI TRACK")
    midifile.addTempo(track, time, tempo)

    channel = 0
    volume = 100

    for note in notes:
        onset = note[0] * (tempo/60.)
        duration = note[1] * (tempo/60.)
        # duration = 1
        pitch = int(note[2])
        midifile.addNote(track, channel, pitch, onset, duration, volume)

    with open(outfile, 'wb') as file:
        midifile.writeFile(file)


def audio_to_midi_melodia(infile, outfile, bpm, smooth=0.25, minduration=0.1, sr=44100, hop=128,
                          savejams=False):
    # load audio using librosa
    print("Loading audio...")
    data, sr = librosa.load(infile, sr=sr, mono=True)

    # extract melody using melodia vamp plugin
    print("Extracting melody f0 with MELODIA...")
    melody = vamp.collect(data, sr, "mtg-melodia:melodia",
                          parameters={"voicing": 1.0})

    # hop = melody['vector'][0]
    pitch = melody['vector'][1]

    # impute missing 0's to compensate for starting timestamp
    pitch = np.insert(pitch, 0, [0] * 8)

    # debug
    # np.asarray(pitch).dump('f0.npy')
    # print(len(pitch))

    # convert f0 to midi notes
    print("Converting Hz to MIDI notes...")
    midi_pitch = hz2midi(pitch)

    # segment sequence into individual midi notes
    notes = midi_to_notes(midi_pitch, sr, hop, smooth, minduration)

    # save note sequence to a midi file
    print("Saving MIDI to disk...")
    save_midi(outfile, notes, bpm)
    #
    # if savejams:
    #     print("Saving JAMS to disk...")
    #     jamsfile = outfile.replace(".mid", ".jams")
    #     track_duration = len(data) / float(fs)
    #     save_jams(jamsfile, notes, track_duration, os.path.basename(infile))
    #
    print("Conversion complete.")
