
NOTE_NAMES = ('A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#')
ALTERNATE_NOTE_NAMES = {'A#':'Bb', 'Db':'C#', 'D#':'Eb', 'Gb':'F#', 'Ab':'G#'}

SHARP = '#'
FLAT  = 'b'

SEMITONE = 2**(1/12)

class Note:
    def __init__(self, name='A', octave=4, cents=0, value=None, tuning=440):
        '''
        Create a note by supplying name, octave, and cents, or value
        note = Note('A', 4, 0.5, tuning=440)
        note = Note(value=35, tuning=440)

        Inputs
            name: name of the note
            octave: octave of the note
            cents: semitone offset

            value: note as an integer, where 0 is A0

            tuning: the frequency of A4
        '''
        
        if name not in NOTE_NAMES and name not in ALTERNATE_NOTE_NAMES:
            raise ValueError('Note name {} is not valid'.format(name))

        if value is None:
            value = self.note2int(name, octave, cents)

        self.value = value
        self.tuning = tuning

    def __str__(self):
        name_str = self.name
        octave_str = str(self.octave)
        cents_str = '{:+.2f}'.format(self.cents) if self.cents != 0 else ''
        return name_str + octave_str + cents_str

    def __repr__(self):
        name_str = self.name
        octave_str = str(self.octave)
        cents_str = '{:+.2f}'.format(self.cents) if self.cents != 0 else ''
        return "Note({}{}{})".format(name_str, octave_str, cents_str)


    @property
    def name(self):
        return NOTE_NAMES[round(self.value)%len(NOTE_NAMES)]

    @property
    def octave(self):
        return round(self.value) // len(NOTE_NAMES)

    @property
    def cents(self):
        return self.value - round(self.value)

    @property
    def frequency(self):
        ref = Note('A', 4).as_int()
        return self.tuning * SEMITONE**(self.value-ref)

    def as_int(self):
        return self.value


    def shift(self, semitones):
        self.value += semitones    
        return self.value

    @staticmethod
    def standard_name(name):
        ''' Returns the default name for the given note 
                For example, will return Bb if given A# or Bb
        '''

        if name in ALTERNATE_NOTE_NAMES:
            name = ALTERNATE_NOTE_NAMES[name]

        return name

    @staticmethod
    def note2int(name, octave, cents):
        ''' Converts a note name to an integer, where A0 is 0, Bb0 is 1, ... '''

        name = Note.standard_name(name)

        name_val = NOTE_NAMES.index(name)
        octave_val = octave * len(NOTE_NAMES)

        return name_val + octave_val + cents


def note_range(tuning=440, start=Note('C',0), end=Note('C',8)):
    '''
    Creates a range of notes from start to end

    notes = note_frequencies(a4 = 440)

    input
        a4: The tuning of a4; affects the tuning of all notes

    output
        notes: a dictionary containing <frequency> : <note> pairs
    '''
    notes = []

    start = start.as_int()
    end = end.as_int()

    for i in range(start, end): 
        notes.append( Note(value=i, tuning=tuning) )

    return notes
