# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
import os
import tkinter as tk
# import pandas as pd
import threading
import signal
import glob
from serial import Serial
from voltage_reader import VoltageReader
from display import DisplayApp

class Logger:
    
    app_root = None

    def get_pi_port():
        res = glob.glob('/dev/ttyACM*')
        return res[0]
    
    PI_PORT = get_pi_port()
    WINDOWS_PORT = 'COM3'
    reading_thread = None

    def __init__(self):
        pass    
    
    def update_plot(readings, lines_data, axs):
        print(readings)

        for i in range(len(readings)):
            lines_data[i].set_data(readings[i][0], readings[i][1])
            axs[i].set_xlim(min(readings[i][0]), max(readings[i][0]))
            axs[i].set_ylim(min(readings[i][1]) - 1, max(readings[i][1]) + 1)

    # def plot_animation(i, v_data: VoltageReader, lines_data, axs):
    #     v_data.readings.use_readings(update_plot, lines_data, axs)

    def int_handler(self, s,t):
        # print(s, t)
        print('Stopping')
        VoltageReader.stop_reading.set()
        Logger.reading_thread.join()
        Logger.app_root.destroy()
        # plt.close()

    def main(self):
        adcs = 3

        # defines DISPLAY variable for tkinter if needed
        if os.environ.get('DISPLAY','') == '':
            print('no display found. Using :0.0')
            os.environ.__setitem__('DISPLAY', ':0.0')
        
        Logger.app_root = tk.Tk()
        app = DisplayApp(Logger.app_root, 3)

        arduino = Serial(port=self.PI_PORT, baudrate=9600, timeout=1)
        # fig, axs = plt.subplots(2, 1)
        # lines_data = [axs[i].plot([], [])[0] for i in range(plots)]

        v_data = VoltageReader(arduino, adcs, app)

        Logger.reading_thread = threading.Thread(target=v_data.read_voltages)
        Logger.reading_thread.start()

        signal.signal(signal.SIGINT, self.int_handler)
        # reading_thread.join()

        # fig.suptitle('Voltage Measurements')
        # frame_count = 0

        # plot_ani = animation.FuncAnimation(
        #     fig, 
        #     plot_animation,
        #     fargs=[v_data, lines_data, axs], 
        #     interval=1000, 
        #     save_count=frame_count, 
        #     cache_frame_data=True
        # )
        # plt.plot([1], [2])
        # plt.show()
        Logger.app_root.mainloop()
    
    def start(self):
        self.main()

if __name__ == '__main__':
    Logger().start()
