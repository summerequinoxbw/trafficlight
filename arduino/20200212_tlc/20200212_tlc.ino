
//Traffic Light Control Box.
//https://www.amazon.ca/uxcell%C2%AE-Mushroom-Emergency-Latching-Station/dp/B008LT328Y/
//Each button is wired to the NO terminal pair using cat5e.

#define pinBrown 0
#define pinOrange 1
#define pinGreen 2
#define pinBlue 3
#define pinLED 13

byte buttonStates[] = {0, 0, 0, 0};

void buttonBrown() {
  buttonStates[0] = 1;
}
void buttonOrange() {
  buttonStates[1] = 1;
}
void buttonGreen() {
  buttonStates[2] = 1;
}
void buttonBlue() {
  buttonStates[3] = 1;
}

void setup() {
  Serial.begin(9600);
  pinMode(pinLED, OUTPUT);

  //All buttons are wired as Normally Open.
  pinMode(pinBrown, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinBrown), buttonBrown, FALLING);
  pinMode(pinOrange, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinOrange), buttonOrange, FALLING);
  pinMode(pinGreen, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinGreen), buttonGreen, FALLING);
  pinMode(pinBlue, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(pinBlue), buttonBlue, FALLING);
}

//If a button is pressed, send a serial message to a waiting network connected host.
void loop() {
  for(byte i = 0; i < 4; i = i + 1) {
    if(buttonStates[i] == 1){
      Serial.print("stat/trafficcontrol/button");
      Serial.print(i);
      Serial.println(" ON");
      digitalWrite(pinLED,HIGH);
      delay(30);
      digitalWrite(pinLED,LOW);
      buttonStates[i] = 0;
    }
  }
  delay(1);
}
