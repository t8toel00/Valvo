#include <SoftwareSerial.h>
SoftwareSerial BTSerial(10,11);

const int pwPin = 2;
#define trigPin 3
#define echoPin 4
#define ARR_SIZE 3
float pulse1, sensor1;
float pulse2, sensor2;

int sensoryht,objekt;
int obj1=0;
int vert;
int objekt_sum;

int arr_objekt[ARR_SIZE];

bool vertFlag;

unsigned long timestart=0,timenow, timeLast = millis();

void setup() {
Serial.begin(9600);
pinMode(pwPin, INPUT);
pinMode(trigPin,OUTPUT);
pinMode(echoPin,INPUT);
BTSerial.begin(9600);
}

void read_sensor()
{
//  objekt_sum = 0;
//  if(0 < objekt && objekt < 165)
//  {
//    // Get average:
//    for(int l=0;l < ARR_SIZE;l++)
//    {
//      digitalWrite(trigPin, LOW);  
//      delayMicroseconds(2); 
//      digitalWrite(trigPin, HIGH);
//      delayMicroseconds(10);
//      digitalWrite(trigPin, LOW);
//      pulse2=pulseIn(echoPin,HIGH);
//      pulse1=pulseIn(pwPin,HIGH);
//      sensor1=pulse1*0.034/2;
//      sensor2=pulse2*0.034/2;
//      sensoryht=sensor1+sensor2;
//      objekt=169-sensoryht;
//      arr_objekt[l] = objekt;
//    }
//  
//    for(int i=0;i<ARR_SIZE;i++)
//    {
//      objekt_sum = objekt_sum + arr_objekt[i];
//    }
//  
//    objekt = objekt_sum / ARR_SIZE;
//    Serial.println(objekt);
//  }
//  else
//  {
      digitalWrite(trigPin, LOW);  
      delayMicroseconds(2); 
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);
      pulse2=pulseIn(echoPin,HIGH);
      pulse1=pulseIn(pwPin,HIGH);
      sensor1=pulse1*0.034/2;
      sensor2=pulse2*0.034/2;
      sensoryht=sensor1+sensor2;
      objekt=169-sensoryht;
//  }
}

void printall()
{
  Serial.println("\nPari");
 Serial.print("Sensor1=");
 Serial.println(sensor1);
  Serial.print("Sensori2=");
   Serial.println(sensor2);
    Serial.print("Leveys=");
     Serial.println(objekt);
     Serial.println(obj1);
}
void bluetooth()
{
  if((millis() - timeLast) > 500)
  {
    BTSerial.print("[");
    BTSerial.print(objekt,DEC);
    BTSerial.print("]");
    timeLast = millis();
  }
}
void vertailu()
{
  vertFlag = false;
  timenow=millis();
  if (((timenow-timestart)>5000) || (obj1==0) || ((-170 < objekt) && (objekt < -150)))
  {
    //Serial.print(obj1);
    Serial.println("time diff ");
    Serial.print(timenow-timestart);
    timestart=millis();
    obj1=objekt;
    vertFlag = true;
  }
   vert=abs(obj1-objekt);
}


void loop()
{
 read_sensor();
 Serial.println(objekt);

   if(0 < objekt && objekt < 165)   
        {
         vertailu();
         if(vert>50)
          {
            printall();
            Serial.println(vert);
            bluetooth();
          }
         else if(vertFlag == true)
         {
            printall();
            Serial.println(vert);
            bluetooth();
         }
        }
  else if(((-170 < objekt) && (objekt < -150)))
    {
      vertailu();
    }
}

