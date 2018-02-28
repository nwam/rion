import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import math
import peakutils
import sys

import pdb

import note as note_lib

fs = 44100

TRUMPET_SAMPLE = 'samples/Trumpet.wav'
TRUMPET_1H_LOW = 800
TRUMPET_1H_HIGH = 1200

OBOE_SAMPLE = 'samples/Oboe.wav'
OBOE_NOTE1_END = 70000
OBOE_1H_LOW = 300
OBOE_1H_HIGH = 500

def note_filter(x):
    '''
    Transfers signal in the time domain into musical note buckets

    X_notes, notes = note_filter(X)

    input
        x: signal in time domain

    output
        X_notes: signal in frequency domain with only musical note buckets
        notes: array of Note objects of len(X_notes) denoting each corresponding note to each bucket in X_notes
    '''

    # Get the list of notes that we will bucket to
    notes = note_lib.note_range(start=note_lib.Note('A', 0), end=note_lib.Note('F', 9))

    # Get the edge frequencies of each note
    note_edges = note_lib.note_range(start=note_lib.Note('A', 0), end=note_lib.Note('F#', 9))
    for note_edge in note_edges:
        note_edge.shift(-0.5)
    note_edges = list(map(lambda n: n.frequency, note_edges))

    # Our output: note buckets
    X_notes = np.zeros(len(notes)) 

    # DFT
    X = np.real(np.fft.fft(x))

    # Fill note buckets
    for i in range(len(notes)):
        note = notes[i]
        edge_low = note_edges[i]
        edge_high = note_edges[i+1]

        # Iterate through frequencies near the current note
        for freq in range(math.floor(edge_low), math.ceil(edge_high)+1):
            similarity = 1/(abs(note.frequency - freq)+1)**(1/12)
            X_notes[i] += abs(X[freq]) * similarity
            if X_notes[i] < 0:
                pass
                #pdb.set_trace()

    return X_notes, notes

if __name__ == '__main__':
    sample_file = TRUMPET_SAMPLE
    
    if len(sys.argv) > 1:
        sample_file = sys.argv[1]

    # Load trumpet sample
    rate, x = scipy.io.wavfile.read(sample_file)
    X = np.fft.fft(x)
    plt.plot(X)
    plt.show()

    X_notes, notes = note_filter(x)
    X_notes = X_notes / max(X_notes)

    peaks = peakutils.indexes(X_notes, thres=0.02/max(X_notes), min_dist=1)

    plt.plot(X_notes)
    plt.scatter(peaks, np.zeros(len(peaks)))
    plt.show()

    peak_notes = [notes[peak] for peak in peaks]
    f_0 = peak_notes[0]
    print(peak_notes)

    peak_tones = [peak_note.name for peak_note in peak_notes]
    modal_tone = max(set(peak_tones), key=peak_tones.count)

    print('f_0 is {} and modal tone is {}'.format(f_0, modal_tone))

    # Save result
    #scipy.io.wavfile.write('TrumpetOut.wav', fs, x)
