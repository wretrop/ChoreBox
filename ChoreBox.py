'''
28May2022 - Will Porter

This was built to track dog chores.  My dogs get 2 feeds a day and 2 walks a day, but my wife and I
would sometimes get mixed up or couldn't remember if the dogs had gotten their due.  I didn't like the thought
that they weren't getting taken care of, so this was a fun little project to try to attack that problem.
Though the focus is on dog chores, it could, of course, be generalized to anything.

This is a pretty simple python script that monitors 4 LED-buttons connected to an RPi Zero W.
When the button is pushed, the button's LED toggles (from off to on or vice versa).
At midnight (according to the Rpi system clock), all the LEDs turn off.  The script simply loops along to
infinity.

Because the recommended voltage to the LEDs was 5V, I didn't power them directly from the RPi logic pins
Instead, there's a relay board in my build that controls output from the RPi 5V rail to the button LEDs.
Honestly, this is overkill considering the relative size and cost of the relay board.  But, it was easy.
If I build a V2, I'll try designing a small PCB that uses small MOSFETs instead.

Button state sensing leverages the 'gpiozero' library.  It took me an embarrassingly long time to figure out how 
to use it, but se la vie.  That's learning!  The multi-threading that happens under the hood is something I need
to get more used to.  I'm more familiar with Arduino ISRs for real-time input and detection.
'''


from gpiozero import Button
from gpiozero import LED
import time
import datetime

debug = False

# Set up GPIO pins
    # 4 inputs for button state sensing
    # 4 outputs to drive LED Power relays (3.3V Logic to drive relay for 5V LED power)

FOOD_INPUT_PIN_1 = 14 # Physical Pin 8 // GPIO 14
LED_POWER_OUTPUT_1 = 17 # Physical Pin 11 // GPIO 17

FOOD_INPUT_PIN_2 = 4 # Physical Pin 7 // GPIO 4
LED_POWER_OUTPUT_2 = 18 # Physical Pin 12 // GPIO 18

WALK_INPUT_PIN_1 = 27 # Physical Pin 13 // GPIO 27
LED_POWER_OUTPUT_3 = 22 # Physical Pin 15 // GPIO 22

WALK_INPUT_PIN_2 = 24 # Physical Pin 18 // GPIO 24
LED_POWER_OUTPUT_4 = 23 # Physical Pin 16 // GPIO 23


def Action_ButtonPush(btn):
    # TODO - Write to database in future    
    # when the button is pushed, toggle the LED
    # DB write changes based on SW state change?
    pass



def time_until_end_of_day(dt=None):
    # type: (datetime.datetime) -> datetime.timedelta
    """
    Get timedelta until end of day on the datetime passed, or current time.
    """
    if dt is None:
        dt = datetime.datetime.now()
    tomorrow = dt + datetime.timedelta(days=1)
    return datetime.datetime.combine(tomorrow, datetime.time.min) - dt

if __name__ == "__main__":
    FoodButton_1 = Button(FOOD_INPUT_PIN_1)
    FoodButton_2 = Button(FOOD_INPUT_PIN_2)
    WalkButton_1 = Button(WALK_INPUT_PIN_1)
    WalkButton_2 = Button(WALK_INPUT_PIN_2)

    FoodLED_1 = LED(LED_POWER_OUTPUT_1)
    FoodLED_2 = LED(LED_POWER_OUTPUT_2)
    WalkLED_1 = LED(LED_POWER_OUTPUT_3)
    WalkLED_2 = LED(LED_POWER_OUTPUT_4)

    time.sleep(0.05)

    FoodButton_1.when_pressed = FoodLED_1.toggle
    FoodButton_2.when_pressed = FoodLED_2.toggle
    WalkButton_1.when_pressed = WalkLED_1.toggle
    WalkButton_2.when_pressed = WalkLED_2.toggle

    for i in range(10):
        FoodLED_1.toggle()
        FoodLED_2.toggle()
        WalkLED_1.toggle()
        WalkLED_2.toggle()
        time.sleep(0.5)


    while True:
        toMidnight = time_until_end_of_day().seconds
        print("Seconds to midnight are: " + str(toMidnight))


        time.sleep(toMidnight)

        # turn off LEDs
        FoodLED_1.off()
        FoodLED_2.off()
        WalkLED_1.off()
        WalkLED_2.off()
