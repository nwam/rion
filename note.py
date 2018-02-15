
NOTE_NAMES = ('A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#')
ALTERNATE_NOTE_NAMES = {'A#':'Bb', 'Db':'C#', 'D#':'Eb', 'Gb':'F#', 'Ab':'G#'}

SHARP = '#'
FLAT  = 'b'

class Note:
    def __init__(self, name='A', octave=4, int=None):
        '''
        Create a note by supplying:
            name and octave, or
            int
        '''
        
        if name not in NOTE_NAMES and name not in ALTERNATE_NOTE_NAMES:
            raise ValueError('Note name {} is not valid'.format(name))

        if int is not None:
            name, octave = self.int2note(int)

        self.name = name
        self.octave = octave

    def __str__(self):
        return self.name + str(self.octave)

    def __repr__(self):
        return "Note({}{})".format(self.name, str(self.octave))

    def standardized(self):
        '''
        Converts a note name into a note name from the list of NOTE_NAMES
        '''
        if self.name in ALTERNATE_NOTE_NAMES:
            return Note(name = ALTERNATE_NOTE_NAMES[self.name], octave = self.octave)

        return Note(name = self.name, octave = self.octave)

    def int(self):
        '''
        Converts a note name to an integer, where A0 is 0
        '''
        note = self.standardized()

        name_val = NOTE_NAMES.index(note.name)
        octave_val = self.octave * len(NOTE_NAMES)

        return name_val + octave_val

    @staticmethod
    def int2note(i):
        octave = i//len(NOTE_NAMES)
        name = NOTE_NAMES[i%len(NOTE_NAMES)]

        return name, octave



def note_frequencies(a4=440, start=Note('C',0), end=Note('C',8)):
    '''
    Calculates the frequencies of each note for a specific tuning
        from C0 to B8

    notes = note_frequencies(a4 = 440)

    input
        a4: The tuning of a4

    output
        notes: a dictionary containing <frequency> : <note> pairs
    '''
    notes = {}

    start = start.int()
    end = end.int()
    ref = Note('A', 4).int()

    semitone = 2**(1/12)

    for i in range(start, end): 
        notes[a4 * semitone**(i-ref)] = Note(int=i)

    return notes
