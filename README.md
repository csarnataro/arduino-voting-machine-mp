# Arduino voting machine

This is a very simple proof-of-concept on how to use an Arduino Nano RP2040 Connect to 
send data to the Arduino Cloud via Micropython.

<img src="https://github.com/csarnataro/arduino-voting-machine-mp/assets/11388820/032b526e-b9f1-4f7a-abc1-dfb978e63257" alt="A simple cardboard voting machine with an Arduino Nano RP2040 inside" width="400">

## What's inside

<img src="https://github.com/csarnataro/arduino-voting-machine-mp/assets/11388820/4c40825a-ad50-47ac-887e-a1d629ca4c69" alt="An Arduino Nano Rp2040 mounted on a breadboard" width="400">

The yellow button corresponds to "JavaScript votes", the blue to "TypeScript votes". And there's a buzzer too!

Each button is connected to its own pin (in [INPUT_PULLUP mode](https://docs.arduino.cc/tutorials/generic/digital-input-pullup/)) and to GND. 

Each time a button is pressed, a vote is sent to the Arduino Cloud.

## Usage

You can setup your environment following the instructions available 
at https://docs.arduino.cc/micropython/micropython-course/course/introduction-arduino/
and https://docs.arduino.cc/arduino-cloud/guides/micropython/

The examples in these documents are mostly using an Arduino Nano ESP32, 
anyway everything should work seamlessly for the Arduino Nano RP2040 as well. 

The basic steps are:
- Install the firmware on your board using the Arduino Micropython installer (see https://labs.arduino.cc/en/labs/micropython-installer)
- Install the Arduino Micropython IDE (see https://labs.arduino.cc/en/labs/micropython) 
- Connect the board to your PC and copy the files in this repo.
- Configure a Thing on the Arduino Cloud console (https://app.arduino.cc), with at least these variables:
  - float jsPercentage;
  - float tsPercentage;
  - int buttonPushCounterJS;
  - int buttonPushCounterTS;
- Configure your Arduino Nano RP2040 as a "manual device" and download the PDF with the secret key
- Download the code of this repo and open it in the Micropython IDE.
- Add the downloaded secret key in file "secrets.py", along with your WiFi credentials
- Connect the board
- Launch the Micropython script and have fun

 
## Licence
MIT