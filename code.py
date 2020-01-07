import time
import board
import adafruit_hcsr04
import digitalio
import pulseio
import sys

# This is the State Machine class that will be inherited from the main one
class SM:
    def start(self):
        self.state = self.startState
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    def transduce(self, inputs):
        self.start()
        return [self.step(inp) for inp in inputs]

# This is the class where we built our own class inheriting State Machine class
class ParkAssistant(SM):
    state = ""
    def __init__(self):
        # defining each item that belongs to our class
        self.second_counter = 0  # local variable as counter
        self.greenLED = digitalio.DigitalInOut(board.D10)  # Green LED
        self.redLED = digitalio.DigitalInOut(board.D11)  # Red LED
        self.yellowLED = digitalio.DigitalInOut(board.D12)  # Yellow LED
        # Opening Ceremony
        for led in [self.greenLED, self.yellowLED, self.redLED]:
            led.direction = digitalio.Direction.OUTPUT
            led.value = False
            time.sleep(2)
            led.value = True
            time.sleep(1)
        self.buzzer = pulseio.PWMOut(board.D13, variable_frequency=True)  # Buffer initiated
        # Buffer attributes - Start
        self.buzzer.frequency = 440
        self.OFF = 0
        self.ON = 2 ** 15
        # Buffer attributes - End
        self.buzzer.duty_cycle = self.ON  # Turn on the buzzer
        time.sleep(1)
        self.buzzer.duty_cycle = self.OFF  # Turn off the buzzer
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D2)  # Sensor placement on board

        print("Obstacle Detector Device is Working")

    def getNextValues(self, state, inp):
        self.inp = inp
        self.state = state  #
        self.turnOffLEDs()  # Turning off the LEDs
        # Conditions are made here to warn the driver
        if inp > 120 and inp < 200:
            self.greenLED.value = False
            return "You are Safe", inp
        elif inp > 50 and inp <= 120:
            self.yellowLED.value = False
            return "Slow Down Your Speed", inp 
        elif inp > 25 and inp <= 50:
            self.redLED.value = False
            return "DANGER TOO CLOSE", inp
        elif inp >= 200:
            self.greenLED.value = False
            self.yellowLED.value = False
            return 'Distance Error', inp
        elif inp <= 25:
            self.redLED.value = False
            self.buzzer.duty_cycle = self.ON
            self.second_counter += 1
            if self.second_counter >= 5:
                self.shutdown()
            return "Warning!", inp
    
    # This function is made to turn off LEDs at a moment
    def turnOffLEDs(self):
        self.redLED.value = True
        self.greenLED.value = True
        self.yellowLED.value = True

    # This function is made to check 
    def VolumeControl(self):
        """ You can open commants to obtain dynamic frequency changing """
        
#         if self.state == "You are Safe" or self.inp >= 120:
#             self.buzzer.duty_cycle = self.OFF
#             return

#         if self.state != "Warning!":
#             self.second_counter = 0
            
#         self.buzzer.duty_cycle = self.ON
#         frequency = 440-self.inp*4
#         if frequency <= 0: frequency = 1
#         self.buzzer.frequency = frequency
        if self.state != "Warning!": self.buzzer.duty_cycle = self.OFF

    # This is the function that starts the whole application
    def startParking(self):
        while True:
            try:
                print("{}: {}".format(self.step(int(self.sonar.distance)), self.state))
                self.VolumeControl()
            except RuntimeError:
                print('Distance Error')
            time.sleep(0.5)
    # This is the function that will stop the whole system at a moment.
    def shutdown(self):
        print("The Device Stopped! Calling the emergency services")
        sys.exit()

parkAssistant = ParkAssistant()  # Forming the instance
parkAssistant.startParking()  # Starting the application
