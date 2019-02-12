// Dependencies
#include <Servo.h>
#include <Time.h>
#include <TimeLib.h>
Servo servoPan;
Servo servoTilt;

// Variables
int servoDelay = 10;
int servoIncrement = 1;
int loopDelay = 100;

// Pins
int panPin = 9;
int tiltPin = 10;
int sensorPin = 11;
char panPotPin = A0;
char tiltPotPin = A1;
int ledPin = 8;
int buttonPin = 2;

// DO NOT TOUCH. Declaring all our global variables.
char incomingByte = 0;
int servoInteract = 0;
int startTime = 0;
int curPos = 0;
bool detected = false;
String command = "";
bool panPot = false;
bool tiltPot = false;

// Button Variables
int buttonTime = 0; 
int buttonState = 0;
int prevButtonState = 1;
bool maintenanceState = false;
bool startCounter = false;

// Handle all the pins being enabled. Attach Servos.

void setup()
{
  Serial.begin(9600);
  servoPan.attach(panPin);
  servoTilt.attach(tiltPin);
  setPins();
}
void setPins()
{
  pinMode(LED_BUILTIN, OUTPUT); 
  pinMode(panPotPin, INPUT_PULLUP);
  pinMode(tiltPotPin, INPUT_PULLUP);
  pinMode(sensorPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
}
// Main Loop.
// We read data. We check detection with PIR sensor.
// We call takeInput to process the data we received.
// We got a delay so that we can send multiple commands in one go.
void loop()
{
  ExtraHardware();
  incomingByte = Serial.read();
  takeInput();
  delay(loopDelay);
}

// Here we look at the input we take in.
// We save the input into a command string.
// However, we don't do this if we receive '-1', since it is "empty"
// Or ';' since that is our end character for commands
// Or for 10 since that is the newline char.
// If we do receive a semicolon, we start processing the command that has been saved.
void takeInput()
{
  if (incomingByte != -1 && incomingByte != ';' && incomingByte != 10) // 10 being the newline char. -1 being the "no info sent" char.
    command += incomingByte;
  else if (incomingByte == ';')
    processCommand();
}
// Test of the PIR Sensor. LED Lights up when it detects. 
// We also start a timer to see if it was turned on in the last 30 seconds.
void PIR()
{
  int currentTime = now();
  if (digitalRead(sensorPin))
  {
    digitalWrite(ledPin, HIGH);
    detected = true;
    startTime = now();
  }
  else
    digitalWrite(ledPin, LOW);
  if ((currentTime - startTime) >= 30)
  {
    digitalWrite(ledPin, LOW);
    detected = false;
  }
}
void ExtraHardware()
{
  PIR();
  if (ButtonMaintenance())
    Pots();
}
bool ButtonMaintenance()
{
  buttonState = digitalRead(buttonPin);
  
  if (buttonState == LOW && prevButtonState == HIGH)
  {
    buttonTime = now(); 
    startCounter = true;
  }
  while (digitalRead(buttonPin) == LOW && startCounter)
  {
      if (((now()) - buttonTime) >= 3)
      {
        maintenanceState = !maintenanceState;
        Serial.println("Maintenance Mode is " + String(maintenanceState));
        Serial.println("Maintenance Mode is " + String(maintenanceState));
        Serial.println("Maintenance Mode is " + String(maintenanceState));
        Serial.println("Maintenance Mode is " + String(maintenanceState));
        Serial.println("Maintenance Mode is " + String(maintenanceState));
        buttonTime = 0;
        startCounter = false;
      }
  }
  prevButtonState = buttonState;
  startCounter = false;
  return maintenanceState;
}
void Pots()
{
  float panSensorValue = map(analogRead(panPotPin), 0, 1023, 0, 200);
  float tiltSensorValue = map(analogRead(tiltPotPin), 0, 1023, 0, 200);
    servoMoveTo(servoPan,panSensorValue);
    servoMoveTo(servoTilt,tiltSensorValue);
}
// It checks the command we got. Then looks up if it matches one of our words in bits.
// Then executes the command.
void processCommand()
{
    if (command == "blank") // Don't touch Servos
      servoInteract = 0;
    else if (command == "panTo") // char for 'pan'
      servoInteract = 1;
    else if (command == "tiltTo") // char for 'tilt'
      servoInteract = 2;
    else if (command == "pan")
      servoInteract = 3;
    else if (command == "tilt")
      servoInteract = 4;
    else if (command == "LED") // char for 'LED'
      switchLED();
    else if (command == "sensor") // char for 'sensor'
      if (detected)
        Serial.write("x");
    else if (command == "readP") // read Pan Angle
      readServo(servoPan);
    else if (command == "readT") // read Tilt Angle
      readServo(servoTilt);
    else if (command.toInt() >= 0 && command.toInt() <= 200)
    {
      if (servoInteract == 1) // if panning to Position
        servoMoveTo(servoPan, command.toInt());
      else if (servoInteract == 2) // if tilting to Position
        servoMoveTo(servoTilt, command.toInt());
      else if (servoInteract == 3) // if panning slowly
        servoMove(servoTilt, command.toInt());
      else if (servoInteract == 4) // if tilting slowly
        servoMove(servoTilt, command.toInt());
      else 
        Serial.println("");
    }
    else
      Serial.println("Command Unknown..");
    command = "";
}
// Read the state of the LED. Then turn it into the opposite state.
// Looks confusing, but it is just an on/off switch.
void switchLED ()
{
    digitalWrite(LED_BUILTIN, !(digitalRead(LED_BUILTIN)));
}

// Take the Servo to move, and the position to move it to.
// Then iterate around it with a for loop.
void servoMove(Servo servo, int pos)
{
  int finalPosition = (servo.read() + pos);
  if (curPos < finalPosition)
    for (int i = curPos; i <= finalPosition; i += servoIncrement)
      servo.write(i);
  else
    for (int i = finalPosition; i >= finalPosition; i -= servoIncrement)
      servo.write(i);
}
void servoMoveTo(Servo servo, int pos)
{
  curPos = servo.read();
  if (curPos < pos)
    for (int i = curPos; i <= pos; i += servoIncrement)
      servo.write(i);
  else
    for (int i = curPos; i >= pos; i -= servoIncrement)
      servo.write(i);
}