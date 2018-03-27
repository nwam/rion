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
    notes = notepy.note_range(start=notepy.Note('A', 0), end=notepy.Note('C', 10))

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

        freq_bucket = note.frequency / (len(x)/fs)
        freq_bucket_low = math.floor(freq_bucket)
        freq_bucket_high = math.ceil(freq_bucket)

        if freq_bucket_high >= len(X):
            break

        X_notes[i] += abs(X[freq_bucket_low]) * (1-abs(freq_bucket - freq_bucket_low))
        X_notes[i] += abs(X[freq_bucket_high]) * (1-abs(freq_bucket - freq_bucket_high)) 
#        edge_low = note_edges[i] * len(x)/fs
#        edge_high = note_edges[i+1] * len(x)/fs
#
#        # Iterate through frequencies near the current note
#        for freq in range(math.floor(edge_low), math.ceil(edge_high)+1):
#            #similarity = 1/(abs(note.frequency - freq)+1)**(1/12)
#            difference = abs(note.as_int() - notepy.Note(frequency=freq/ (len(x)/fs)).as_int())
#            similarity = 1 if difference < 0.05 else 0
#            X_notes[i] += (abs(X[freq])) * similarity
#
#        # Normalize to the size (width) of the bucket
#        X_notes[i] /= (edge_high - edge_low)

    return np.array(X_notes), notes

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

def octave_normalize(note_volumes):
    '''
    Given the volumes of each note, this returns the volumes, normalized to the total volume of the surrounding octave

    normed_volumes, octave_volumes = octave_normalize(note_volumes)

    Input
        note_volumes: 1-D array of volumes of each note

    Output
        normed_volumes: Volume of each note as a ratio of its surrounding octave
        octave_volumes: Total volume of each surrounding octave
        
    '''

    # Full octave kernel
    kernel = np.ones(notepy.OCTAVE + 1)

    # Sum the volumes of the surrounding octave
    oct_sums = np.convolve(note_volumes, kernel, 'same')

    # Count the notes involved in the convolution
    conv_counts = [min(i, len(note_volumes)-i-1, len(kernel)//2) + len(kernel)//2+1 for i in range(len(note_volumes))]

    # Get the normalized total of the surrounding octave
    oct_totals = oct_sums * len(kernel)/conv_counts

    normed_volumes = np.divide(note_volumes, oct_totals, out=np.zeros_like(note_volumes), where= oct_totals!=0)

    return normed_volumes, oct_totals
