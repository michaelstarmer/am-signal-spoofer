from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np
import time

from db import query

RECEIVED_SIGNAL = [[], []]
MAX_DURATION = 3
RECEIVE_PIN = 27
MEASURES = [[], []]

TIMESTAMP = int(time.time())

LOG_PATH = '../workspace/signal-log.txt'
EXPORT_PATH = '../workspace/signal-export.csv'
GRAPH_PATH = '../workspace/graph.png'

if __name__ == '__main__':

    def save_data(MEASURES):
        res = query("SELECT * FROM signals")
        print("Res:", res)
        for row in res:
            print(row)
        
        csv = open(EXPORT_PATH, 'w+')
        csv.write('timestamp,output\n')

        for i in range(len(MEASURES[0])):
            csv_line = "{},{}\n".format(MEASURES[0][i], MEASURES[1][i])
            csv.write(csv_line)
        csv.close()

        return True

    def capture_ticks(signalInterceptNo):
        if GPIO.input(RECEIVE_PIN):
            signalInterceptNo += 1
        time_delta = datetime.now() - beginning_time

        current_input = GPIO.input(RECEIVE_PIN)

        # all TRUE inputs is logged with timestamp
        if current_input:
            MEASURES[0].append(time_delta)
            MEASURES[1].append(current_input)

        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        
        cumulative_time = time_delta.seconds


    def show_summary(signals_no):
        print('\n** Ended recording **')
        print(len(RECEIVED_SIGNAL[0]), 'samples recorded')
        print("{} intercepts in this job.".format(signals_no))

    def generate_graph():
        print("\n** Plotting results **")
        plt.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
        plt.axis([0, MAX_DURATION, -1, 2])
        plt.savefig(GRAPH_PATH)

        return plt
        
    def show_graph(plt):
        print("\n** Displaying graph **")
        plt.show()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN)
    
    cumulative_time = 0
    beginning_time = datetime.now()
    signalInterceptNo = 0

    print("**Started recording**")
    while cumulative_time < MAX_DURATION:
        if GPIO.input(RECEIVE_PIN):
            signalInterceptNo += 1
        time_delta = datetime.now() - beginning_time

        current_input = GPIO.input(RECEIVE_PIN)

        # all TRUE inputs is logged with timestamp
        if current_input:
            MEASURES[0].append(time_delta)
            MEASURES[1].append(current_input)

        RECEIVED_SIGNAL[0].append(time_delta)
        RECEIVED_SIGNAL[1].append(GPIO.input(RECEIVE_PIN))
        
        cumulative_time = time_delta.seconds

    show_summary(signalInterceptNo)
    GPIO.cleanup()

    print("\n**Processing results**")

    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    # nparray = np.array(MEASURES)
    # np.savetxt('signal-log.txt', nparray, delimiter='\n')
    
    gen_graph = generate_graph()

    if save_data(RECEIVED_SIGNAL):
        show_graph(gen_graph)
