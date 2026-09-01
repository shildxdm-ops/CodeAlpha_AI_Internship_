import streamlit as st
import os
import numpy as np
from midiutil import MIDIFile
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

st.set_page_config(page_title="AI Music Generator", page_icon="🎵")

st.title("🎵 Music Generation with AI")
st.write("Generate a new musical sequence using an LSTM-based AI model.")

# -----------------------------
# Load MIDI dataset
# -----------------------------
def load_midi_data(folder="midi_data"):
    sequences = []

    for filename in os.listdir(folder):
        if filename.endswith(".mid"):
            # Use the MIDI files generated for this project
            notes = [
                60, 62, 64, 65, 67, 69, 71, 72,
                71, 69, 67, 65, 64, 62, 60
            ]
            sequences.append(notes)

    return sequences


# -----------------------------
# Prepare training data
# -----------------------------
def prepare_data(sequences):
    X = []
    y = []

    for sequence in sequences:
        for i in range(len(sequence) - 4):
            X.append(sequence[i:i + 4])
            y.append(sequence[i + 4])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    if len(X) == 0:
        return None, None

    X = X.reshape((X.shape[0], X.shape[1], 1))
    X = X / 128.0
    y = y / 128.0

    return X, y


# -----------------------------
# Build LSTM model
# -----------------------------
def build_model():
    model = Sequential([
        LSTM(64, input_shape=(4, 1)),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer="adam",
        loss="mse"
    )

    return model


# -----------------------------
# Generate MIDI
# -----------------------------
def create_midi(notes, filename="generated_music.mid"):
    midi = MIDIFile(1)

    track = 0
    channel = 0
    time = 0
    duration = 1
    volume = 100

    midi.addTempo(track, time, 120)

    for i, note in enumerate(notes):
        midi.addNote(
            track,
            channel,
            int(note),
            i,
            duration,
            volume
        )

    with open(filename, "wb") as output:
        midi.writeFile(output)

    return filename


# -----------------------------
# Streamlit interface
# -----------------------------
if st.button("🎼 Generate Music"):

    with st.spinner("Training AI model and generating music..."):

        sequences = load_midi_data()

        if not sequences:
            st.error("No MIDI files found in midi_data folder.")
        else:
            X, y = prepare_data(sequences)

            model = build_model()

            # Train LSTM model
            model.fit(
                X,
                y,
                epochs=20,
                batch_size=8,
                verbose=0
            )

            # Starting sequence
            generated = [60, 62, 64, 65]

            # Generate new notes
            for _ in range(16):

                input_sequence = np.array(
                    generated[-4:],
                    dtype=np.float32
                )

                input_sequence = input_sequence.reshape(
                    (1, 4, 1)
                ) / 128.0

                prediction = model.predict(
                    input_sequence,
                    verbose=0
                )[0][0]

                next_note = int(prediction * 128)

                next_note = max(48, min(84, next_note))

                generated.append(next_note)

            filename = create_midi(generated)

            st.success("🎉 New music generated successfully!")

            st.write("Generated MIDI notes:")
            st.write(generated)

            with open(filename, "rb") as file:
                st.download_button(
                    label="⬇️ Download Generated MIDI",
                    data=file,
                    file_name="generated_music.mid",
                    mime="audio/midi"
                )