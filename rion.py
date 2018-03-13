import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import math
import peakutils
import sys
import ltfatpy

import pdb

import note as notepy

def note_filter(x, fs=44100):
    '''
    Transfers a signal in the time domain into musical note buckets

    X_notes, notes = note_filter(x)

    input
        x: signal in time domain

    output
        X_notes: signal in frequency domain with only musical note buckets
        notes: array of Note objects of len(X_notes) 
            denoting each corresponding note to each bucket in X_notes
    '''

    # Get the list of notes that we will bucket to
    notes = notepy.note_range(start=notepy.Note('C', 0), end=notepy.Note('C', 10))

    # Get the edge frequencies of each note
    note_edges = notepy.note_range(start=notepy.Note('C', 0), end=notepy.Note('C#', 10))
    for note_edge in note_edges:
        note_edge.shift(-0.5)
    note_edges = list(map(lambda n: n.frequency, note_edges))

    # Our output: note buckets
    X_notes = np.zeros(len(notes)) 

    # DFT
    X = np.real(np.fft.fft(x))
    X = X[:len(X//2)]

    # Fill note buckets
    for i in range(len(notes)):
        note = notes[i]
        edge_low = note_edges[i] * len(x)/fs
        edge_high = note_edges[i+1] * len(x)/fs

        # Iterate through frequencies near the current note
        for freq in range(math.floor(edge_low), math.ceil(edge_high)+1):
            similarity = 1/(abs(note.frequency - freq)+1)**(1/12)
            X_notes[i] += (abs(X[freq])) * similarity

        # Normalize to the size (width) of the bucket
        X_notes[i] /= (edge_high - edge_low)

    return X_notes, notes

def get_notes(x, fs=44100):
    '''
    Gets the peaks in the fft and 
    returns a list of the corresponding note and magnitude of each peak

    notes = get_notes(x, fs=44100)

    inputs
        x: signal in time domain
        fs: sampling rate

    output
        notes: a list of Note objects of the detected note
        magnitudes: a list of len(notes) with the magnitudes of notes
    '''

    notes = []
    magnitudes = []
    
    X = np.fft.fft(x)
    X = X[ : math.ceil(len(X)/2) ]
    X = X/np.max(X)

    peaks = peakutils.indexes(X, thres=0.55/max(X), min_dist=5)

    for peak in peaks:
        freq = peak * len(x)/fs
        note = notepy.Note(frequency=freq)
        magnitude = X[peak]

        notes.append(note)
        magnitudes.append(np.real(magnitude))

    return magnitudes, notes
