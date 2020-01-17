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
PREDICTION = []

TIMESTAMP = int(time.time())

LOG_PATH = '../generated/signal-log.txt'
EXPORT_PATH = '../generated/signal-export.csv'
GRAPH_PATH = '../generated/graph.png'

if __name__ == '__main__':

    def categorize(MEASURES):
        res = query("SELECT * FROM signals")
        print("Res:", res)
        for row in res:
            print(row)
        return False
        csv = open(EXPORT_PATH, 'w+')
        csv.write('timestamp,output\n')

        for i in range(len(MEASURES[0])):
            csv_line = "{},{}\n".format(MEASURES[0][i], MEASURES[1][i])
            csv.write(csv_line)
        csv.close()
        return True

        for i in range(len(MEASURES[1])):
            curr_timestamp = MEASURES[0][i]
            prev_timestamp = MEASURES[0][i-1] if MEASURES[0][i-1] else curr_timestamp
            diff_timestamp = curr_timestamp - prev_timestamp
            prev_timestamp_str = "{}:{}".format(str(prev_timestamp.seconds), str(prev_timestamp.microseconds))
            curr_timestamp_str = "{}:{}".format(str(curr_timestamp.seconds), str(curr_timestamp.microseconds))
            diff_timestamp_str = "{}".format(str(diff_timestamp.microseconds))

            s = "{} (prev) | {} (curr) | {} (diff, ms)\n".format(prev_timestamp_str, curr_timestamp_str, diff_timestamp_str)
            #s = "{},{},{}\n".format(str(prev_timestamp), str(curr_timestamp), str(diff_timestamp))
            csv_string = "{},{},{}\n".format(str(prev_timestamp), str(curr_timestamp), str(diff_timestamp))

            logdiff = curr_timestamp - prev_timestamp
            diff_in_ms = logdiff.microseconds
            category = 'Unknown'
            line = ''
            if diff_in_ms > 50:
                if diff_in_ms > 250 and diff_in_ms < 400:
                    category = 3
                    line = str(category) + ' -> ' + s
                elif diff_in_ms > 1200 and diff_in_ms < 1500:
                    category = 2
                    line = str(category) + ' -> ' + s
                elif diff_in_ms > 2300 and diff_in_ms < 2800:
                    category = 1
                    line = str(category) + ' -> ' + s
                elif diff_in_ms > 9000 and diff_in_ms < 9500:
                    line = '\n** BLOCK BREAK\n** ' + s + '** BLOCK BREAK\n\n'

                print('Line', line)
                csv.write(csv_string)
            

        csv.close()

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

    print('\n**Ended recording**')
    print(len(RECEIVED_SIGNAL[0]), 'samples recorded')
    print("{} intercepts in this job.".format(signalInterceptNo))

    GPIO.cleanup()

    print("\n**Processing results**")

    
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] = RECEIVED_SIGNAL[0][i].seconds + RECEIVED_SIGNAL[0][i].microseconds/1000000.0

    # nparray = np.array(MEASURES)
    # np.savetxt('signal-log.txt', nparray, delimiter='\n')
    
    if categorize(RECEIVED_SIGNAL):
        print("\n**Plotting results**")
        
        plt.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
        plt.axis([0, MAX_DURATION, -1, 2])
        plt.savefig(GRAPH_PATH)
        plt.show()

    # fig = plt.figure(figsize=[70, 2], dpi=300)
    # plt.tight_layout()
    # plt.savefig(GRAPH_PATH)
    # plt.close(fig)

