import wasp

class NoteApp():

    NAME = 'NOTE'

    def __init__(self):
        self._file_contents: bytes = None
        self.finished: bool = True

    def foreground(self):
        if self._file_contents is None:
            with open('note', 'rb') as f:
                self._file_contents = f.read()
        wasp.system.request_event(wasp.EventMask.TOUCH)
        self._draw()
        self._update()

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        draw.string('Note App', 0, 10, width=240)
        draw.string('Tap to play', 0, 30, width=240)

    def _update(self):
        string = wasp.watch.drawable.string
        if self.finished:
            string("Not playing", 0, 60, width=240)
        else:
            string("Playing", 0, 60, width=240)

    def touch(self, _event):
        if self.finished:
            self._update()
            self._note()

    def _play(length, note):
        notes = {
            14: 8,
            13: 10,
            12: 30,
            11: 45,
            10: 47,
            9: 50,
            8: 55,
            7: 60,
            6: 67,
            5: 70,
            4: 72,
            3: 74,
            2: 75,
            1: 77,
            0: 80,
        }
        wasp.watch.vibrator.pulse(duty=notes[note], ms=length*10)

    def _note(self):
        assert self._file_contents[0:4] == b'Note', "Not a note file!"
        ptr = 4
        while ptr < len(self._file_contents) - 1:
            length = self._file_contents[ptr]
            note = self._file_contents[ptr + 1]
            NoteApp._play(length, note)
            ptr += 2
        self.finished = True
            
        

