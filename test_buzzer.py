from machine import Pin, PWM
import utime

BUZZER_PIN = 21  # GPIO21 => PIN 9

# Define Servo Pin, PWM object and position offset
buzzer_pin = Pin(BUZZER_PIN)
buzzer_pwm = PWM(buzzer_pin)

def tone(buzzer, frequency):
    # Set maximum volume
    buzzer.duty_u16(2048)
    # Play tone
    buzzer.freq(frequency)


def no_tone(buzzer):
    buzzer.duty_u16(0)


while True:
    tone(buzzer_pwm, 440)
    time.sleep_ms(100)  
    no_tone(buzzer_pwm)
  
    tone(buzzer_pwm, 440 * 2)
    time.sleep_ms(100)  
    no_tone(buzzer_pwm)
  
    time.sleep_ms(500)  
    
    tone(buzzer_pwm, 440 * 2)
    time.sleep_ms(100)  
    no_tone(buzzer_pwm)
  
    tone(buzzer_pwm, 440)
    time.sleep_ms(100)  
    no_tone(buzzer_pwm)

    time.sleep_ms(1500)  
