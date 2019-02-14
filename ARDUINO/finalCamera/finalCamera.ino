// Dependencies
#include <Servo.h>
//#include <Time.h>
#include <TimeLib.h>
Servo servoPan;
Servo servoTilt;

// Variables
int servoDelay = 10;
int servoIncrement = 1;
int loopDelay = 100;

// Pins
int panPin = 10;
int tiltPin = 9;
int sensorPin = 11;
int pictureLED = 5;
int maintenanceLED = 3;
int sensorLED = 4;
int buttonPin = 2;
char panPotPin = A0;
char tiltPotPin = A1;

// DO NOT TOUCH. Declaring all our global variables.
char incomingByte = 0;
int servoInteract = 0;
int startTime = 0;
String command = "";
bool panPot = false;
bool tiltPot = false;
bool detected = false;


// Button Variables
//int buttonTime = 0; 
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
  pinMode(pictureLED, OUTPUT);
  pinMode(maintenanceLED, OUTPUT);
  pinMode(sensorLED, OUTPUT);

  
  pinMode(panPotPin, INPUT_PULLUP);
  pinMode(tiltPotPin, INPUT_PULLUP);
  pinMode(sensorPin, INPUT);
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
    digitalWrite(sensorLED, HIGH);
    detected = true;
    startTime = now();
  }
  else
    digitalWrite(sensorLED, LOW);
  
  if ((currentTime - startTime) >= 30)
    detected = false;
      //digitalWrite(sensorLED, LOW);
}
// Just exists to call our Button and Sensor functions. Checks regularly if they are active.
void ExtraHardware()
{
  PIR();
  if (ButtonMaintenance())
    Pots();
}
// Function for handling our button. If it is clicked for longer than 3 seconds
// we then enter "Maintenance" Mode. This also makes an LED blink so the user knows
// in Maintenance Mode, the user can use Potentiometers to adjust the camera.
bool ButtonMaintenance()
{
  buttonState = digitalRead(buttonPin);
  int buttonTime = 0
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
  if (maintenanceState)
  {
    switchLED(maintenanceLED);
    delay(100);
  }
  prevButtonState = buttonState;
  startCounter = false;
  return maintenanceState;
}

// Function for sending the Potentiometer data to the servos.
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
    if (command == "panTo") 
      servoInteract = 1;
    else if (command == "tiltTo") 
      servoInteract = 2;
    else if (command == "pan")
      servoInteract = 3;
    else if (command == "tilt")
      servoInteract = 4;
    else if (command == "LED") 
      switchLED(LED_BUILTIN);
    else if (command == "sensor") 
    {
      if (detected)
      {
        Serial.write("x");
      }
    }
    else if (command == "picture")
    {
      Serial.println("picture");
      switchLED(pictureLED);
      delay(300);
      switchLED(pictureLED);
      delay(300);
    }
    else if (command.toInt() >= -200 && command.toInt() <= 200)
    {
      if (servoInteract == 1) // if panning to Position
        servoMoveTo(servoPan, command.toInt());
      else if (servoInteract == 2) // if tilting to Position
        servoMoveTo(servoTilt, command.toInt());
      else if (servoInteract == 3) // if panning slowly
        servoMove(servoPan, command.toInt());
      else if (servoInteract == 4) // if tilting slowly
        servoMove(servoTilt, command.toInt());
    }
    else
      Serial.println("Command Unknown..");
    command = "";
}
// Read the state of the LED. Then turn it into the opposite state.
// Looks confusing, but it is just an on/off switch.
void switchLED (int LED)
{
    digitalWrite(LED, !(digitalRead(LED)));
}


// Take the Servo to move, and the amount of degrees to move (pos).
// Then iterate around it with a for loop.
void servoMove(Servo servo, int pos)
{
  int finalPosition = (servo.read() + pos);
  int curPos = servo.read();
  if (curPos < finalPosition)
    for (int i = curPos; i <= finalPosition; i += servoIncrement)
      servo.write(i);
  else
    for (int i = finalPosition; i >= finalPosition; i -= servoIncrement)
      servo.write(i);
}
// Take the Servo to move, and the position to move it to.
// Then iterate around it with a for loop.
void servoMoveTo(Servo servo, int pos)
{
  int curPos = servo.read();
  if (curPos < pos)
    for (int i = curPos; i <= pos; i += servoIncrement)
      servo.write(i);
  else
    for (int i = curPos; i >= pos; i -= servoIncrement)
      servo.write(i);
}
