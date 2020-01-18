from datetime import datetime
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv, sys, os
import pandas as pd

# input
EXPORT_PATH = "../workspace/signal-export.csv"

# output
OUTPUT_PATH = '../generated'
SIGNATURE_PATH = '../generated/transmit-signature.csv'
LOG_PATH = '../generated/transmit-signature.log'

NUM_ATTEMPTS = 7
TRANSMIT_PIN = 27

bar_width = 0.00020
block_break = 0.09316

sm_delay = 0.00034
md_delay = 0.00330
lg_delay = 0.01340

if __name__ == '__main__':
    def open_export(path):
        print("\n** Processing data **")
        values = [[], []]
        x = []
        y = []
        emptyValueCounter = []
        set_output_no = 0
        unset_output_no = 0

        with open(path, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            try:
                for i, row in enumerate(reader):
                    if i == 0: continue # skip header
                    float_x = float(row[0])
                    int_y = int(row[1])

                    if len(emptyValueCounter) > 10000:
                        print("EmptyValueCounter contains more than 2000. Deleting.")
                        for value in emptyValueCounter:
                            del x[emptyValueCounter[0]:emptyValueCounter[-1]]
                            del y[emptyValueCounter[0]:emptyValueCounter[-1]]
                        emptyValueCounter.clear()
                    else:
                        x.append(float_x)
                        y.append(int_y)
                
                print('Encoding successful.')
                for i in range(len(x)):
                    if y[i] == 1:
                        set_output_no += 1 
                    else:
                        unset_output_no += 1
                print("\nNumber of raw ticks:\t {}".format(set_output_no))
                return [x,y]
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(path, reader.line_num, e))

    def create_graph(x, y):
        print("\n** Creating graph **")

        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis([0, 3, -1, 2])
        plt.show()

    def replicate_pattern(x,y):
        signal_pattern = [[], []] # signal duaration, signal value
        signal_series = []
        signal_length = 0

        signal_log = []
        signatures = [[], []]
        
        for i in range(len(x)):
            
            if len(y) < i+2:
                # end of data file
                break

            if y[i] == 1:
                signal_series.append(x[i])
                if len(y) < i+1:
                    print("Signal data 1 end.")
                    break
                elif y[i+1] != 1:
                    signal_length = signal_series[-1] - signal_series[0]
                    signal_pattern[0].append(signal_length)
                    signal_pattern[1].append(1)

                    seconds = int(signal_length)
                    microseconds = (signal_length * 1000000) % 1000000
                    log = "{} -> {} \t- {} \t| {} \t-> {}s, {}ms".format('1', round(signal_series[0], 6), round(signal_series[-1], 6),round(signal_length, 6), round(seconds, 6), round(microseconds, 6))
                    signal_log.append(log)
                    signatures[0].append(1)
                    signatures[1].append(signal_length)
                    signal_series.clear()
            elif y[i] == 0:
                signal_series.append(x[i])
                if len(y) < i+1:
                    print("Signal data 0 end.")
                    break
                elif y[i+1] == 1:
                    signal_length = signal_series[-1] - signal_series[0]
                    signal_pattern[0].append(signal_length)
                    signal_pattern[1].append(0)
                  
                    seconds = int(signal_length)
                    microseconds = (signal_length * 1000000) % 1000000
                    log = "{} -> {} \t- {} \t| {} \t-> {}s, {}ms".format('0', round(signal_series[0], 6), round(signal_series[-1], 6),round(signal_length, 6), round(seconds, 6), round(microseconds, 6))
                    signal_log.append(log)
                    signatures[0].append(0)
                    signatures[1].append(signal_length)
                    signal_series.clear()

        return [signatures, signal_log]
        #return signal_pattern

    def write_data(signature_data, log_data):

        signal_path = '{}/{}'.format(OUTPUT_PATH, '')

        if sys.argv[1:]:
            try:
                # /transmit-signature.csv
                signal_path = '{}/{}'.format(OUTPUT_PATH, sys.argv[1])
                os.makedirs(signal_path)
            except OSError:
                print("Create directory %s failed" % signal_path)
            else:
                print("Signal folder creation success: %s" % signal_path)

        signature_log = '{}/signature.log'.format(signal_path)
        signature_csv = '{}/signature.csv'.format(signal_path)

        print("Saving signal to path:", signal_path)
        logfile = open(signature_log, 'w+')
        for entry in range(len(log_data)):
            logline = "{}\n".format(log_data[entry])
            logfile.write(logline)
        logfile.close()

        sigfile = open(signature_csv, 'w+')
        for index in range(len(signature_data[0])):
            signatureline = "{},{}\n".format(signature_data[1][index], signature_data[0][index])
            sigfile.write(signatureline)
        sigfile.close()

        print("Encoded signal length:\t {}\n".format(len(log_data)))

        return True

    def display_signal_preview(signal_pattern):
        signal_durations = signal_pattern[0]
        signal_values = signal_pattern[1]

        for i in range(50):
            print("Signal {}: {}".format(signal_values[i], signal_durations[i]))

    csv_values = open_export(EXPORT_PATH)
    signal = replicate_pattern(csv_values[0], csv_values[1])
    write_data(signal[0], signal[1])
    
    # display_signal_preview(signal)