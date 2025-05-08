import mido
import threading
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from control import CsoundControl

# Your existing code
cs = CsoundControl()

sliders = {
    "freq": {"from": 0.1, "to": 20, "value": 3},
    "cutoff": {"from": 10, "to": 5000, "value": 200},
    "res": {"from": 0.0, "to": 1.0, "value": 0.5},
    "combVerbTime": {"from": 0.1, "to": 10.0, "value": 3.0},
    "combLooptime": {"from": 0.1, "to": 10.0, "value": 1.5},
    "combRes": {"from": 0.0, "to": 1.0, "value": 0.5},
    "combMix": {"from": 0.0, "to": 1.0, "value": 0.5},
}

pitchwheel_to_slider = {
    0: "freq",
    1: "cutoff",
    2: "res",
    3: "combVerbTime",
    4: "combLooptime",
    5: "combRes",
    6: "combMix"
}


def scale_midi_to_slider(midi_val, slider_min, slider_max):
    norm = (midi_val + 8192) / 16380  # Normalize to 0.0 - 1.0
    return slider_min + norm * (slider_max - slider_min)


def update_slider(slider_name, value, send_feedback=False):
    slider_info = sliders[slider_name]
    from_, to_ = slider_info["from"], slider_info["to"]
    value = max(min(value, to_), from_)
    slider_info["value"] = value
    cs.update_channel(slider_name, value)

    if send_feedback:
        send_midi_feedback(slider_name, value)


def send_midi_feedback(slider_name, value):
    channel_map = {
        "freq": 0,
        "cutoff": 1,
        "res": 2,
        "combVerbTime": 3,
        "combLooptime": 4,
        "combRes": 5,
        "combMix": 6
    }

    channel = channel_map.get(slider_name)
    if channel is not None:
        midi_value = int((value - sliders[slider_name]["from"]) / (
            sliders[slider_name]["to"] - sliders[slider_name]["from"]) * 16384 - 8192)

        midi_value = max(min(midi_value, 8191), -8192)

        with mido.open_output(find_xtouch_port()) as outport:
            msg = mido.Message('pitchwheel', channel=channel, pitch=midi_value)
            outport.send(msg)


def find_xtouch_port():
    for port in mido.get_input_names():
        if 'X-TOUCH' in port.upper() or 'BEHRINGER' in port.upper():
            return port
    return None


def listen_to_xtouch():
    port_name = find_xtouch_port()
    if not port_name:
        print("Behringer X-Touch port not found.")
        return

    with mido.open_input(port_name) as inport:
        print(f"Listening to MIDI input on: {port_name}")
        print("Press Ctrl+C to stop.")
        for msg in inport:
            if msg.type == 'pitchwheel':
                channel = msg.channel
                value = msg.pitch

                if channel in pitchwheel_to_slider:
                    slider_name = pitchwheel_to_slider[channel]
                    scaled_value = scale_midi_to_slider(
                        value, sliders[slider_name]["from"], sliders[slider_name]["to"])
                    update_slider(slider_name, scaled_value,
                                  send_feedback=True)
                else:
                    print(
                        f"Unhandled MIDI pitchwheel message on channel {channel}: {value}")


def start_midi_listener():
    midi_thread = threading.Thread(target=listen_to_xtouch, daemon=True)
    midi_thread.start()

# Animation function using matplotlib and scipy


# Placeholder sliders dictionary, assuming your actual sliders dictionary
sliders = {
    "freq": {"from": 0.1, "to": 20, "value": 3},
    "cutoff": {"from": 10, "to": 5000, "value": 200},
    "res": {"from": 0.0, "to": 1.0, "value": 0.5},
    "combVerbTime": {"from": 0.1, "to": 10.0, "value": 3.0},
    "combLooptime": {"from": 0.1, "to": 10.0, "value": 1.5},
    "combRes": {"from": 0.0, "to": 1.0, "value": 0.5},
    "combMix": {"from": 0.0, "to": 1.0, "value": 0.5},
}


def animate_feedback(i, bars, value_texts, axes):
    for ax, bar, text, (name, slider) in zip(axes, bars, value_texts, sliders.items()):
        val = slider["value"]
        bar[0].set_height(val)  # Update bar height
        text.set_text(f"{val:.2f}")  # Update label text
        text.set_y(val + (slider["to"] * 0.05))  # Adjust label position
    # Return patches and texts
    return [patch for bar in bars for patch in bar] + value_texts


def setup_animation():
    num_sliders = len(sliders)
    fig, axes = plt.subplots(1, num_sliders, figsize=(
        2.2 * num_sliders, 4), sharey=False)

    if num_sliders == 1:
        axes = [axes]

    bars = []
    value_texts = []

    for ax, (name, slider) in zip(axes, sliders.items()):
        val = slider["value"]
        bar = ax.bar([0], [val], width=0.5, color='cornflowerblue')
        text = ax.text(0, val + (slider["to"] * 0.05),
                       f"{val:.2f}", ha='center', va='bottom')

        ax.set_ylim(slider["from"], slider["to"])
        ax.set_title(name)
        ax.set_xticks([])
        bars.append(bar)
        value_texts.append(text)

    plt.tight_layout()
    ani = FuncAnimation(fig, animate_feedback, fargs=(
        bars, value_texts, axes), interval=200, blit=False)
    plt.show()


# Thread to run the animation
# Run the MIDI listener and animation concurrently
if __name__ == "__main__":
    # Start MIDI listener in the background
    start_midi_listener()

    # Run the animation in the main thread (required for macOS)
    setup_animation()

# start_midi_listener()
# start_animation()

# To keep the script running
while True:
    pass
