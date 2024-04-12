import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
import threading
import signal
from voltage_reader import VoltageReader

def update_plot(readings, lines_data, axs):
    print(readings)

    for i in range(len(readings)):
        lines_data[i].set_data(readings[i][0], readings[i][1])
        axs[i].set_xlim(min(readings[i][0]), max(readings[i][0]))
        axs[i].set_ylim(min(readings[i][1]) - 1, max(readings[i][1]) + 1)


def plot_animation(i, v_data: VoltageReader, lines_data, axs):
    v_data.readings.use_readings(update_plot, lines_data, axs)


def int_handler(s,t):
    # print(s, t)
    print('Stopping')
    VoltageReader.stop_reading.set()
    reading_thread.join()
    plt.close()

if __name__ == '__main__':
    
    plots = 3

    arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
    fig, axs = plt.subplots(2, 1)
    # lines_data = [axs[i].plot([], [])[0] for i in range(plots)]

    v_data = VoltageReader(arduino, plots)

    reading_thread = threading.Thread(target=v_data.read_voltages)
    reading_thread.start()

    signal.signal(signal.SIGINT, int_handler)
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
    while not VoltageReader.stop_reading.is_set():
        pass
        
