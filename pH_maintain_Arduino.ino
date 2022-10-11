byte input;

const int analogInPin = A0;
unsigned long int allValue;
float b = 21.984;
float m = -5.6183;
// pHValue = m * pHVolt + b

int buf[1000], temp;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  input = Serial.read();

  if (input == '1'){
    for(int i=0;i<1000;i++){
      buf[i] = analogRead(analogInPin);
      delay(60);
      
    }
    //get 50 datas from pH sensor
  
    for(int i=0;i<999;i++){
      for(int j=i+1;j<1000;j++){
        if(buf[i]>buf[j]){
          temp = buf[i];
          buf[i] = buf[j];
          buf[j] = temp;
        
        }
      }
    }
    //50 datas are arranged in from lowest to highest

    allValue = 0;
  
    for(int i=451;i<551;i++){
      allValue += buf[i]; 
    }
    //20 datas from 16th to 35th are added as "allValue"

    float pHVolt = (float)allValue * 5 / 1024 / 100;
    //convert from analog value to voltage
  
    float pHValue = m * pHVolt + b;
    //convert from voltage to pH value

    Serial.println(pHValue);
    delay(20);
  }
}
