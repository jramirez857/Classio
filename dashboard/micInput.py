import pyaudio
import struct
import math
import RPi.GPIO as GPIO
import time
import statistics

GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
CHANNELS = 1 #2
RATE = 48000#44100
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)

def get_rms( block ):
    # RMS amplitude is defined as the square root of the
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into
    # a string of 16-bit samples...

    # we will get one short out for each
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768.
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

class ClarityRating(object):
    def __init__(self, limit):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.threshold = limit   #above this means too quiet
        self.recentDB = []
        self.thresholdSize = 60 #100 = 5 seconds
        self.errorcount = 0


    def stop(self):
        self.stream.close()

    def find_input_device(self):
        device_index = None
        for i in range( self.pa.get_device_count() ):
            devinfo = self.pa.get_device_info_by_index(i)
            print( "Device %d: %s"%(i,devinfo["name"]) )

            for keyword in ["mic","input","dsnooped"]:
                if keyword in devinfo["name"].lower():
                    print( "Found an input: device %d - %s"%(i,devinfo["name"]) )
                    device_index = i
                    return device_index

        if device_index == None:
            print( "No preferred input found; using default input device." )

        return device_index

    def open_mic_stream( self ):
        device_index = self.find_input_device()

        stream = self.pa.open(   format = FORMAT,
                                 channels = CHANNELS,
                                 rate = RATE,
                                 input = True,
                                 input_device_index = device_index,
                                 frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

        return stream

    def updateList(self, value):
        if (len(self.recentDB) == self.thresholdSize):
            del self.recentDB[-1]
            self.recentDB.insert(0,value)
        # TODO:     ELIF PROF CORRECTS THEMSELF, CLEAR ARRAY !
        else:
            self.recentDB.insert(0,value)

    def status(self):
        if (statistics.mean(CR.recentDB) > self.threshold):
            print("TOO QUIET!") #Update LEDs here
            GPIO.output(19,True)
            GPIO.output(22,False)
            
        else:
            print("good boy")
            GPIO.output(22,True)
            GPIO.output (19,False)

    def listen(self):
        try:
            block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        except IOError as e:
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            return

        amplitude = get_rms( block )

        dB = abs(20 * math.log(amplitude, 10))

        self.updateList(dB)


def run(threshold):
    CR = ClarityRating(threshold)

    while True:
        CR.listen()
        CR.status()
        time.sleep(0.05)      # 20 Hz????

    #print(CR.recentDB)
    #print(statistics.mean(CR.recentDB))
