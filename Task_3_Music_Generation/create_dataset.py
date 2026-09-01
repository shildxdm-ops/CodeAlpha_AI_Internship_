from midiutil import MIDIFile
import os

os.makedirs("midi_data", exist_ok=True)

for song_no in range(5):
    midi = MIDIFile(1)
    track = 0
    channel = 0
    time = 0
    duration = 1
    tempo = 120
    volume = 100

    midi.addTempo(track, time, tempo)

    notes = [
        60, 62, 64, 65, 67, 69, 71, 72,
        71, 69, 67, 65, 64, 62, 60
    ]

    for i, note in enumerate(notes):
        midi.addNote(
            track,
            channel,
            note + song_no,
            time + i,
            duration,
            volume
        )

    filename = f"midi_data/song_{song_no + 1}.mid"

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)

print("5 MIDI files created successfully!")