import LED
import time
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
    startState = 'ON'
    def __init__(self):
        self.redLED = LED(17)
        self.greenLED = LED(16)
        self.yellowLED = LED(15)
        for led in [self.redLED, self.greenLED, self.yellowLED]:
            led.on()
            time.sleep(2)
            led.off()
            time.sleep(1)
        self.buzzer = LED(14)
        print("Obstacle Detector Device is Working")
        self.startParking()
    
    def getNextValues(self, inp):
        self.turnOffLEDs()
        if inp > 120 and inp < 200:
            self.greenLED.on()
            print("You are Safe")
        elif inp > 50 and inp < 120:
            self.yellowLED.on()
            print("Slow Down Your Speed")
        elif inp > 25 and inp < 50:
            self.redLED.on()
            print("DANGER TOO CLOSE")
        elif inp > 200:
            self.greenLED.on()
            self.yellowLED.on()
        elif inp < 25:
            self.redLED.on()
            self.buzzer.on()
            print("The Device Stopped! Calling the emergency services")
            self.shutdown()
    
    def turnOffLEDs(self):
        self.redLED.off()
        self.greenLED.off()
        self.yellowLED.off()

    def startParking(self):
        while True:
            inp = "test"
            self.getNextValues(inp)
    def shutdown(self):
        exit()