import tkinter as tk

class DisplayApp:
    def __init__(self, root: tk.Tk, adcs):
        self.root = root
        root.configure(background='black')
        self.master = root
        master = self.master

        # self.mainframe = tk.Frame(self.master, padx='10', pady='10')
        # self.measures = [tk.Label(self.mainframe, text=f'V: 0') for i in range(adcs)]
        root.attributes('-fullscreen', True)  # Fullscreen mode
        root.bind('<Escape>', self.quit_fullscreen)  # Bind escape key to exit fullscreen

        self.m_labels = []

        self.section1 = tk.Frame(master, background='black', pady=50)
        self.section1.pack(side=tk.TOP, pady=20)
        self.label1a = tk.Label(self.section1, text="0 V", font=("Helvetica", 108), fg='#fff', bg='#000')
        self.label1a.pack(side=tk.LEFT, padx=10)

        self.label1b = tk.Label(self.section1, text="0", font=("Helvetica", 108), fg='#fff', bg='#000')
        self.label1b.pack(side=tk.LEFT, padx=10)

        self.m_labels.append((self.label1a, self.label1b))

        self.section2 = tk.Frame(master, background='black', pady=50)
        self.section2.pack(side=tk.TOP, pady=20)
        self.label2a = tk.Label(self.section2, text="0 V", font=("Helvetica", 108), fg='#fff', bg='#000')
        self.label2a.pack(side=tk.LEFT, padx=10)

        self.label2b = tk.Label(self.section2, text="0", font=("Helvetica", 108), fg='#fff', bg='#000')
        self.label2b.pack(side=tk.LEFT, padx=10)

        self.m_labels.append((self.label2a, self.label2b))

        self.section3 = tk.Frame(master, background='black', pady=50)
        self.section3.pack(side=tk.TOP, pady=20)
        self.label3a = tk.Label(self.section3, text="0 V", font=("Helvetica", 108), fg='#fff', bg='#000')

        self.label3a.pack(side=tk.LEFT, padx=10)
        self.label3b = tk.Label(self.section3, text="0", font=("Helvetica", 108), fg='#fff', bg='#000')
        self.label3b.pack(side=tk.LEFT, padx=10)
        
        self.m_labels.append((self.label3a, self.label3b))

    def update_measurements(self, data):
        for i, (v,c) in enumerate(data):
            self.mod_label(self.m_labels[i][0], v, 'V')
            self.mod_label(self.m_labels[i][1], c, 'Amps')
        pass

    def mod_label(self, label, measurement, unit):
        label.config(text=f"{measurement} {unit}")

    def quit_fullscreen(self, event):
        self.root.attributes('-fullscreen', False)
        self.root.destroy()
