import tkinter as tk
from tkinter import ttk
from control import CsoundControl  # No need to import randomize_parameters here


cs = CsoundControl()
root = tk.Tk()
root.title("Oscillator + Filter Control")

slider_length = 1400
sliders = {}  # Store variables and widgets for programmatic access


def create_slider(name, label, from_, to_, initial, resolution=0.1):
    var = tk.DoubleVar(value=initial)

    def update(val):
        v = float(val)
        cs.update_channel(name, v)
        lbl.config(text=f"{label}: {v:.2f}")
        entry_var.set(f"{v:.2f}")  # Keep entry field in sync

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=5, fill="x")

    top = tk.Frame(frame)
    top.pack(fill="x")

    lbl = tk.Label(top, text=f"{label}: {initial:.2f}")
    lbl.pack(side="left")

    entry_var = tk.StringVar(value=f"{initial:.2f}")
    entry = ttk.Entry(top, textvariable=entry_var, width=10)
    entry.pack(side="right", padx=5)

    def apply_entry(*args):
        try:
            val = float(entry_var.get())
            val = max(min(val, to_), from_)  # Clamp to slider bounds
            var.set(val)
            update(val)
        except ValueError:
            pass  # Ignore invalid input

    entry.bind("<Return>", apply_entry)
    entry.bind("<FocusOut>", apply_entry)

    s = ttk.Scale(frame, from_=from_, to=to_,
                  variable=var,
                  orient="horizontal",
                  length=slider_length,
                  command=update)
    s.pack()

    def jump_to_click(event):
        slider_x = s.winfo_rootx()
        click_x = event.x_root - slider_x
        proportion = min(max(click_x / slider_length, 0), 1)
        value = from_ + proportion * (to_ - from_)
        var.set(value)
        update(value)

    s.bind("<Button-1>", jump_to_click)

    sliders[name] = {
        "var": var,
        "from": from_,
        "to": to_,
        "label": lbl,
        "update": update,
        "scale": s,
        "entry_var": entry_var,
    }


# Sliders
create_slider("freq", "Oscillator Frequency", 0.1, 20, 3)
create_slider("cutoff", "Filter Cutoff", 10, 5000, 200)
create_slider("res", "Resonance", 0.0, 1.0, 0.5, resolution=0.01)
create_slider("combVerbTime", "Comb Reverb Time",
              0.1, 10.0, 3.0, resolution=0.01)
create_slider("combLooptime", "Comb Loop Time",
              0.1, 10.0, 1.5, resolution=0.01)
create_slider("combRes", "Res", 0.0, 1.0, 0.5, resolution=0.01)
create_slider("combMix", "Mix", 0.0, 1.0, 0.5, resolution=0.01)


# Randomization function triggered by the button
def on_randomize():
    cs.randomize_parameters(sliders)  # Using the method from the cs object


# Randomize button
rand_btn = ttk.Button(root, text="Randomize Parameters", command=on_randomize)
rand_btn.pack(pady=10)


def on_close():
    cs.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
