# I would have loved to call this module 'utilities' but apparently it would 
# conflict with an existing builtin module
from machine import Pin, PWM
from time import sleep_ms

def play(buzzer_pwm, frequency = 440, duration = 200):
    # Set volume
    buzzer_pwm.duty_u16(2048)
    # Play tone
    buzzer_pwm.freq(frequency)
    sleep_ms(duration)
    buzzer_pwm.duty_u16(0)


def tone(buzzer_pwm, frequency = 440):
    # Set volume
    buzzer_pwm.duty_u16(2048)
    # Play tone
    buzzer_pwm.freq(frequency)

def no_tone(buzzer_pwm):
    buzzer_pwm.duty_u16(0)

def two_increasing_tones(buzzer_pwm):
    play(buzzer_pwm, 440, 100)
    play(buzzer_pwm, 440 * 3, 100)

def two_decreasing_tones(buzzer_pwm):
    play(buzzer_pwm, 440 * 3, 100)
    play(buzzer_pwm, 440, 100)

def blink(builtin_led, times = 2):
    for i in range(times):
      builtin_led.on()
      sleep_ms(100)
      builtin_led.off()
      sleep_ms(100)

__all__ = ['blink', 'two_decreasing_tones', 'two_increasing_tones']

if __name__ == "__main__":
  builtin_led = Pin(ONBOARD_LED, Pin.OUT)  # GPIO6 => PIN 13
  blink(builtin_led)
  buzzer_pin = Pin(BUZZER_PIN, Pin.OUT)
  buzzer_pwm = PWM(buzzer_pin)
  two_increasing_tones(buzzer_pwm)
  sleep_ms(1000)
  two_decreasing_tones(buzzer_pwm)
