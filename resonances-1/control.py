import ctcsound
import threading
import random


class CsoundControl:
    def __init__(self):
        self.cs = ctcsound.Csound()
        self.cs.setOption("-odac1")  # Use MacBook Pro speakers
        self.cs.setOption("-d")      # Disable displays
        self.cs.setOption("-m0")     # Suppress console messages

        self.cs.compile_('csound', 'resonances-1.csd')
        self.cs.start()
        self.cs.readScore("i1 0 -1")  # -1 for indefinite duration

        self.cs.setControlChannel("freq", 3.0)
        self.cs.setControlChannel("cutoff", 1000.0)
        self.cs.setControlChannel("res", 0.5)
        self.cs.setControlChannel("combVerbTime", 3.0)
        self.cs.setControlChannel("combLooptime", 1.5)
        self.cs.setControlChannel("combRes", 0.5)
        self.cs.setControlChannel("combMix", 0.5)

        self.perform_thread = threading.Thread(target=self.cs.perform)
        self.perform_thread.daemon = True
        self.perform_thread.start()

    def update_channel(self, name, value):
        self.cs.setControlChannel(name, value)

    def randomize_parameters(self, sliders):
        for name, info in sliders.items():
            new_val = random.uniform(info["from"], info["to"])
            info["var"].set(new_val)
            info["entry_var"].set(f"{new_val:.2f}")
            info["update"](new_val)

    def close(self):
        self.cs.stop()
        self.cs.cleanup()
