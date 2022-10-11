
byte  input;

const int analogInPin = A0;
unsigned long int allValue;
int buf[1000], temp;


void setup() {
 Serial.begin(9600);

}


void loop() {
  input = Serial.read();

  if (input == '1'){
    for(int i=0;i<1000;i++){
      buf[i] = analogRead(analogInPin);
      delay(60);
      
    }
  
    for(int i=0;i<999;i++){
      for(int j=i+1;j<1000;j++){
        if(buf[i]>buf[j]){
          temp = buf[i];
          buf[i] = buf[j];
          buf[j] = temp;
        
        }
      }
    }

    allValue = 0;
  
    for(int i=451;i<551;i++){
      allValue += buf[i]; 
    }

    float pHVolt = (float)allValue * 5 / 1024 / 100;

    Serial.print("sensor = ");
    Serial.println(pHVolt);
    delay(20);
    
  }
}
