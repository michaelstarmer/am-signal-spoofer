from datetime import datetime
import time
import sys, csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import numpy as np

MAX_DURATION = 3

NUM_ATTEMPTS = 2
TRANSMIT_PIN = 17

bar_width = 0.00020
block_break = 0.09316

sm_delay = 0.00034
md_delay = 0.00330
lg_delay = 0.01340

control_measures = [[], []]

def logTransmission(output, delta_time):
    control_measures[0].append(delta_time)
    control_measures[1].append(output)

def load_signature(path):
    x = []
    y = []
    with open(path, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        try:
            for i, row in enumerate(reader):
                if i == 0: continue # skip header
                float_x = float(row[0])
                int_y = int(row[1])

                x.append(float_x)
                y.append(int_y)

            print('File loaded.')
            return [x,y]
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(path, reader.line_num, e))


def transmit_code(in_signal = None):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    arg = ''
    if in_signal:
        arg = '{}/'.format(in_signal)

    fpath = '../generated/{}signature.csv'.format(arg)

    print("Transmitting signature:", fpath)

    code = load_signature(fpath)
    
    start_time = datetime.now()

    for t in range(NUM_ATTEMPTS):
        print("Transmitting signal (attempt {})".format(t+1))

        delta_time = datetime.now() - start_time

        for i in range(len(code[0])):
            seconds = int(code[0][i])
            microseconds = (code[0][i] * 1000000) % 1000000
            
            if code[1][i] == 1:
                GPIO.output(TRANSMIT_PIN, 1)
            elif code[1][i] == 0:
                GPIO.output(TRANSMIT_PIN, 0)
            else:
                print("Found neither 1 or 2. Error?")
                continue

            time.sleep(code[0][i])
            
    GPIO.cleanup()

if __name__ == '__main__':

    try:
        if sys.argv[1:]:
            for arg in sys.argv[1:]:
                print("ARG:", arg)
                transmit_code(arg)
                time.sleep(0.5)
        else:
            transmit_code()

        print("Success")
        sys.stdout.flush()
        
    except:
        e = sys.exc_info()[0]
        print(e)
        sys.stdout.flush()
    
    # for arg in sys.argv[1:]:
    #     exec('transmit_code(' + str(arg) + ')')

    #     print("** Plotting results **")
    #     for i in range(len(control_measures[0])):
    #         control_measures[0][i] = control_measures[0][i].seconds + control_measures[0][i].microseconds/1000000.0
        
    #     plt.plot(control_measures[0], control_measures[1], 'go--', linewidth=bar_width)
    #     plt.axis([0, MAX_DURATION, -1, 2])
        
    #     plt.show()