#define LM35 A0 // define a label for "A0" pin

void setup() {
  // put your setup code here, to run once:

  // Use Serial interface for connecting Arduino
  // to an app in the computer
  Serial.begin(9600); // Serial connection speed: 9600bps
  
  // The LM35 follows a linear scale with a 10 mV/ºC factor
  // so the max value of its output analog voltage 
  // is supposed to be 1.5V at 150ºC (the maximum detectable temperature by LM35)
  // which is small compared to the default analog voltage reference of Arduino (5V)
  //
  // So we modify the resolution of the ADC (thus reducing the quantization error)
  // by changing the analog voltage reference of the ADC to 3.3V, 
  // which is a voltage reference available in the Arduino board.
  analogReference(EXTERNAL); // connect AREF pin to 3.3V pin
  
  // NEVER, EVER connect AREF pin to an external voltage reference
  // if analogReference() is not called BEFORE analogRead()
  // or you will create an internal shotcut between the external voltage reference
  // and the default analog voltage reference (5V)
}

void loop() {
  // put your main code here, to run repeatedly:

  // Read the output of the LM35.
  //
  // The ADC has a resolution of 10bit (1024 levels)
  // so it returns an int between 0 and 1023.
  //
  // Since we are using a 3.3V external voltage reference
  // the ADC resolution is: 3.3V / 1024 levels = 3.22mV
  // So, an analog reading between 0 and 3.33mV will be represented by 0, 
  // between 3.22mV and 6.44mV by 1, 
  // between 6.44mV and 9.66mV by 2,
  // ...
  // and between 3.2967V and 3.3V by 1023.
  //
  // All the possible voltage readings within a level, 
  // each of them representing a different temperature, 
  // are coded as if they represented the same temperature.
  int ADC_reading = analogRead(LM35);

  // If we had used the default analog voltage reference (5V)
  // the ADC resolution would have been: 5.0V / 1024 levels = 4.88mV
  // So, an analog reading between 0 and 4.88mV will be represented by 0, 
  // between 4.88mV and 9.76mV by 1, 
  // between 9.76mV and 14.64mV by 2,
  // ...
  // and between 4.99512V and 5V by 1023.
  
  // Convert the ADC reading to voltage
  float voltage = ADC_reading * 3.3/1024; 
  
  // The error between the real voltage read by the ADC
  // and the actual voltage calculated from the int asigned by the ADC 
  // is the quantization error.
  //
  // Thus, we accomplish more accuracy in the readings
  // by reducing the gap between levels.
  
  // Calculate the temperature.
  // LM35 datasheet specifies a linear scale of 10 mV/ºC
  float temperature = voltage * 100;
  
  // Send the temperature to the app in the computer
  Serial.println(temperature);
  
  delay(5000); // Wait 1s between readings to avoid LM35 self-heating
}
