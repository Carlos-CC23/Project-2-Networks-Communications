import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")  # Use the TkAgg backend for embedding in Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# ----- Encoding Functions -----
def nrz_encode(data: str) -> str:
    return ''.join('H' if bit == '1' else 'L' for bit in data)

def nrzi_encode(data: str, initial: str = 'L') -> str:
    current = initial
    encoded = current
    for bit in data:
        if bit == '1':
            current = 'H' if current == 'L' else 'L'
        encoded += current
    return encoded

def manchester_encode(data: str) -> str:
    encoded = ""
    for bit in data:
        if bit == '0':
            encoded += "LH"
        elif bit == '1':
            encoded += "HL"
        else:
            raise ValueError("Data should contain only '0' or '1'")
    return encoded

# ----- Plotting Helpers -----
def map_signal_to_levels(encoded_signal: str):
    return [1 if s == 'H' else 0 for s in encoded_signal]

def create_step_data(levels):
    x = []
    y = []
    for i, val in enumerate(levels):
        x.append(i)   # Start of step
        y.append(val)
        x.append(i+1) # End of step
        y.append(val)
    return x, y

def plot_signal(ax, bit_data: str, encoding_name: str):
    # Encode
    if encoding_name == 'NRZ':
        encoded = nrz_encode(bit_data)
    elif encoding_name == 'NRZI':
        encoded = nrzi_encode(bit_data)
    elif encoding_name == 'Manchester':
        encoded = manchester_encode(bit_data)
    else:
        raise ValueError(f'Unknown encoding: {encoding_name}')

    # Convert to levels
    levels = map_signal_to_levels(encoded)
    x, y = create_step_data(levels)

    ax.step(x, y, where='post', label=encoding_name)
    ax.set_ylim(-0.2, 1.2)
    ax.set_xlim(0, len(levels))

    # Customizing grid lines
    ax.set_xticks(range(len(levels) + 1))
    ax.set_yticks([0, 1])
    ax.grid(True, linestyle='--', alpha=0.7)

    # Optional: Hide axis labels and spines
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.legend(loc='upper right')

# ----- The Main GUI Class -----
class EncodingProjectGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Encoding Waveform Project")

        # ------- OVERVIEW SECTION -------
        overview_frame = ttk.Frame(self.root, padding=10)
        overview_frame.pack(side=tk.TOP, fill=tk.X)

        overview_label = ttk.Label(
            overview_frame,
            text=(
                "Welcome to the Encoding Waveform Project!\n\n"
                "This tool demonstrates three different encoding schemes:\n"
                "1. NRZ (Non-Return to Zero)\n"
                "2. NRZI (Non-Return to Zero, Inverted)\n"
                "3. Manchester Encoding\n\n"
                "Simply enter a binary string below, and click 'Enter' to see the encoded outputs."
            )
        )
        overview_label.pack()

        # ------- INPUT & BUTTONS SECTION -------
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(input_frame, text='Enter Binary Data: ').pack(side=tk.LEFT)
        self.data_var = tk.StringVar()
        self.data_entry = ttk.Entry(input_frame, textvariable=self.data_var, width=50)
        self.data_entry.pack(side=tk.LEFT, padx=5)

        submit_button = ttk.Button(input_frame, text='Enter', command=self.show_results)
        submit_button.pack(side=tk.LEFT)

        # ------- OUTPUT TEXT SECTION -------
        self.output_frame = ttk.Frame(self.root, padding=10)
        self.output_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.output_label = ttk.Label(self.output_frame, text='', justify=tk.LEFT)
        self.output_label.pack(anchor='w')

        # ------- FIGURE SECTION -------
        self.figure_frame = ttk.Frame(self.root)
        self.figure_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig = plt.Figure(figsize=(7, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.figure_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def show_results(self):
        # Clear old text and figure
        self.output_label.config(text='')
        self.fig.clear()

        bit_data = self.data_var.get().strip()
        # Validate input
        if not bit_data:
            messagebox.showerror('Error', 'Please enter binary data.')
            return
        if any(b not in '01' for b in bit_data):
            messagebox.showerror('Error', 'Data should contain only 0s and 1s.')
            return

        # Generate textual results
        nrz_enc = nrz_encode(bit_data)
        nrzi_enc = nrzi_encode(bit_data)
        man_enc = manchester_encode(bit_data)

        result_text = (
            f"NRZ:         {nrz_enc}\n"
            f"NRZI:        {nrzi_enc}\n"
            f"Manchester:  {man_enc}\n"
        )
        self.output_label.config(text=result_text)

        # Create subplots for each encoding
        ax_nrz = self.fig.add_subplot(311)
        ax_nrzi = self.fig.add_subplot(312)
        ax_manchester = self.fig.add_subplot(313)

        plot_signal(ax_nrz, bit_data, 'NRZ')
        plot_signal(ax_nrzi, bit_data, 'NRZI')
        plot_signal(ax_manchester, bit_data, 'Manchester')

        self.fig.tight_layout()
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = EncodingProjectGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
