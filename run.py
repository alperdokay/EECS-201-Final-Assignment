import time
import board
import adafruit_hcsr04
import digitalio
import pulseio


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

class ParkAssistant(SM):
    startState = ''
    def __init__(self):
        self.greenLED = digitalio.DigitalInOut(board.D10)
        self.redLED = digitalio.DigitalInOut(board.D11)
        self.yellowLED = digitalio.DigitalInOut(board.D12)
        for led in [self.redLED, self.greenLED, self.yellowLED]:
            led.direction = digitalio.Direction.OUTPUT
            led.value = True
            time.sleep(1)
            led.value = False
            time.sleep(1)
        self.buzzer = pulseio.PWMOut(board.D13, variable_frequency=True)
        self.buzzer.frequency = 440
        OFF = 0
        ON = 2**15
        self.buzzer.duty_cycle = ON
        time.sleep(1)
        self.buzzer.duty_cycle = OFF
        self.sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D2)

        print("Obstacle Detector Device is Working")
        self.startParking()

    def getNextValues(self, inp):
        self.turnOffLEDs()
        if inp > 120 and inp < 200:
            self.greenLED.value= True
            print("You are Safe")
            return "You are Safe"
        elif inp > 50 and inp < 120:
            self.yellowLED.value = True
            print("Slow Down Your Speed")
            return "Slow Down Your Speed"
        elif inp > 25 and inp < 50:
            self.redLED.value=True
            print("DANGER TOO CLOSE")
            return "DANGER TOO CLOSE"
        elif inp > 200:
            self.greenLED.value = True
            self.yellowLED.value = True
        elif inp < 25:
            self.redLED.value = True
            # self.buzzer.on()
            print("The Device Stopped! Calling the emergency services")
            self.shutdown()

    def turnOffLEDs(self):
        self.redLED.value = False
        self.greenLED.value = False
        self.yellowLED.value = False

    def startParking(self):
        while True:
            try:
                print((self.sonar.distance))
                self.getNextValues(self.sonar.distance)
            except RuntimeError:
                break
            except NameError:
                break
            time.sleep(0.1)
#             inp = "test"
#             self.getNextValues(inp)
    def shutdown(self):
        exit()

# sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D2)

parkAssistant = ParkAssistant()

# while True:
#     try:
#         print((sonar.distance))
#     except RuntimeError as e:
#         print()
#     time.sleep(0.1)
