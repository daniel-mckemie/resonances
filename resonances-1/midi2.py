import mido


def find_xtouch_port():
    """Find the MIDI input/output port that matches Behringer X-Touch"""
    for port in mido.get_input_names():
        if 'X-TOUCH' in port.upper() or 'BEHRINGER' in port.upper():
            return port
    return None


def listen_to_xtouch(port_name):
    """Open the MIDI input and output ports and echo messages back"""
    with mido.open_input(port_name) as inport, mido.open_output(port_name) as outport:
        print(f"Listening to and echoing on: {port_name}")
        print("Press Ctrl+C to stop.")
        for msg in inport:
            print(msg)

            # Only echo messages that affect fader position
            if msg.type in ('pitchwheel', 'control_change'):
                outport.send(msg)


def main():
    port = find_xtouch_port()
    if port:
        listen_to_xtouch(port)
    else:
        print("Behringer X-Touch port not found.")


if __name__ == "__main__":
    main()
