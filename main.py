import network
import logging
import useful_things

from machine import Pin, PWM
from time import sleep_ms

from arduino_iot_cloud import ArduinoCloudClient
from arduino_iot_cloud import Task
from arduino_iot_cloud import async_wifi_connection

# WIFI_SSID and WIFI_PASS are loaded automatically by async_wifi_connection function
from secrets import DEVICE_ID
from secrets import CLOUD_PASSWORD

from useful_things import play as play_pwm
from useful_things import blink
from useful_things import two_increasing_tones as startup_tone
from useful_things import two_decreasing_tones as connection_tone


# See https://docs.arduino.cc/micropython/basics/board-examples/#gpio-map for PIN numbers
BUTTON_PIN_TS = 17  # GPIO17 => PIN 5
BUTTON_PIN_JS = 19  # GPIO19 => PIN 7
BUZZER_PIN = 21  # GPIO21 => PIN 9
ONBOARD_LED = 6  # GPIO6 => PIN 13
BUTTON_PRESSED = 0
BUTTON_UNPRESSED = 1

button_pin_JS = Pin(BUTTON_PIN_JS, Pin.IN, Pin.PULL_UP)
button_pin_TS = Pin(BUTTON_PIN_TS, Pin.IN, Pin.PULL_UP)
buzzer_pin = Pin(BUZZER_PIN, Pin.OUT)
buzzer_pwm = PWM(buzzer_pin)
builtin_led = Pin(ONBOARD_LED, Pin.OUT)  # GPIO6 => PIN 13

button_state_JS = BUTTON_UNPRESSED
button_state_TS = BUTTON_UNPRESSED
last_button_state_JS = BUTTON_UNPRESSED
last_button_state_TS = BUTTON_UNPRESSED
is_connected_to_cloud = False


def on_js_percentage_change(client, value):
  logging.info(f"on_js_percentage_change {value}")

def on_ts_percentage_change(client, value):
  logging.info(f"on_ts_percentage_change {value}")

def on_button_push_counter_TS_change(client, value):
  logging.info(f"on_button_push_counter_TS_change {value}")


def on_button_push_counter_JS_change(client, value):
  logging.info(f"on_button_push_counter_JS_change {value}")

def arduino_client_start():
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=CLOUD_PASSWORD
    )

    # Register Cloud objects.
    # Note: The following objects must be created first in the dashboard and linked to the device.
    # This Cloud object is initialized with its last known value from the Cloud. When this object is updated
    # from the dashboard, the on_switch_changed function is called with the client object and the new value.

    client.register("jsPercentage", on_write=on_js_percentage_change)
    client.register("tsPercentage", on_write=on_ts_percentage_change)
    client.register("buttonPushCounterJS", on_write=on_button_push_counter_JS_change)
    client.register("buttonPushCounterTS", on_write=on_button_push_counter_TS_change)

    client.register(Task("loop", on_run=loop, interval=0.01))

    # This function is registered as a background task to reconnect to WiFi if it ever gets
    # disconnected. Note, it can also be used for the initial WiFi connection, in synchronous
    # mode, if it's called without any args (i.e, async_wifi_connection()) at the beginning of
    # this script.
    client.register(
        Task("wifi_connection", on_run=async_wifi_connection, interval=10.0)
    )
    # Start the Arduino Cloud client.
    client.start()

def play(frequency, duration=200):
  play_pwm(buzzer_pwm, frequency, duration)


def startup_blink():
  blink(builtin_led, 4)  


# mimicing setup
def setup():
    print("**** SETUP ****")
    
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s %(message)s",
        level=logging.DEBUG,
    )

    logging.info("in setup")
    startup_blink()  
    startup_tone(buzzer_pwm)
    connection_tone(buzzer_pwm)
    logging.info("end of setup")

def update_percentages(client, js_votes, ts_votes):
  logging.info(f"JS votes: {js_votes} - TS votes: {ts_votes}")
  js_votes = 0 if js_votes is None else js_votes
  ts_votes = 0 if ts_votes is None else ts_votes
  if (js_votes + ts_votes > 0):
    js_percentage = js_votes / (js_votes + ts_votes) * 100
    ts_percentage = ts_votes / (js_votes + ts_votes) * 100
    logging.info(f"JS%: {js_percentage} - TS%: {ts_percentage}")
    client["jsPercentage"] = js_percentage
    client["tsPercentage"] = ts_percentage
  else:
    client["jsPercentage"] = 0.0
    client["tsPercentage"] = 0.0

def loop(client):  
    # mimicing loop
    global button_state_JS
    global last_button_state_JS
    global button_state_TS
    global last_button_state_TS
    button_state_JS = button_pin_JS.value()
    button_state_TS = button_pin_TS.value()

    if button_state_JS != last_button_state_JS:
        if button_state_JS == BUTTON_PRESSED:
            # if the current state is HIGH then the button went from off to on
            builtin_led.on()
            remote_value = client["buttonPushCounterJS"]
            logging.info("remote value JS is: %d", -1 if remote_value is None else remote_value)
            remote_value = 1 if remote_value is None else remote_value + 1 
            client["buttonPushCounterJS"] = remote_value
            logging.info("ON: number of button pushes JS: %d", client["buttonPushCounterJS"])
            update_percentages(client, client["buttonPushCounterJS"], client["buttonPushCounterTS"]);
            play(2 * 440, 200)

    if button_state_TS != last_button_state_TS:
        if button_state_TS == BUTTON_PRESSED:
            # if the current state is HIGH then the button went from off to on
            builtin_led.on()
            remote_value = client["buttonPushCounterTS"]
            logging.info("remote value TS is: %d", -1 if remote_value is None else remote_value)
            remote_value = 1 if remote_value is None else remote_value + 1
            client["buttonPushCounterTS"] = remote_value
            logging.info("ON: number of button pushes TS: %d", client["buttonPushCounterTS"])
            update_percentages(client, client["buttonPushCounterJS"], client["buttonPushCounterTS"]);
            play(4 * 440, 200)
    
    sleep_ms(50)
    builtin_led.off()
    last_button_state_JS = button_state_JS
    last_button_state_TS = button_state_TS


if __name__ == "__main__":
    setup()
    arduino_client_start()
