#define LED_MAIN 15

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_MAIN, OUTPUT);
  Serial.begin(9600);  // Initialize serial communication
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(LED_MAIN, HIGH);  // Turn LED on
    } 
    else if (command == '0') {
      digitalWrite(LED_MAIN, LOW);   // Turn LED off
    }
  }
}
