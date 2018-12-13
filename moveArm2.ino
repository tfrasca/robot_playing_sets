#include "SerialCommand.h"
#include "ax12.h"

int setArray[] = {-1, -1, -1};
String setPos = "";
bool reading = 0;
String fullString = "";


void setup(){
  Serial.begin(115200);
  pinMode(1, OUTPUT);
  pinMode(2, INPUT);
  SetCompliancewMargin(2);
  torqueOn();
  homePosition();
  }

void loop(){
  
  //serts will be sent in as 'pos1,pos2,pos3'
  // for testing code will read in from serial port
  int button;
  button = digitalRead(2);
  
  if(button == 1){
    Serial.write("button press\n");
    delay(15000);
    relax();
    while(Serial.available()) {
        setArray[0] = -1;
        setArray[1] = -1;
        setArray[2] = -1;
        char character = Serial.read();
        fullString = fullString +  character;
      }    
    Serial.write("picB\n");
  }else if (Serial.available()) {
      while(Serial.available()) {
        setArray[0] = -1;
        setArray[1] = -1;
        setArray[2] = -1;
        char character = Serial.read();
        fullString = fullString +  character;
      }
      
  }else if(fullString != ""){
          int j = 0;
          int w;
          for(w = 0; w < sizeof(fullString); w++){
            if(fullString[w] == ','){
              if(j == 0){  
                setArray[0] = setPos.toInt();
            }else if(j = 1){
                setArray[1] = setPos.toInt();
            }
             j = j++;
             setPos = "";
            }else{
             setPos = setPos + fullString[w];
            }
          }
        
        setArray[2] = setPos.toInt();
        
        torqueOn();
        
        center();
        delay(1000);
        goTo(setArray[0]);
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        winPile();
        delay(3000);
        letGo();
        
        center();
        delay(1000);
        goTo(setArray[1]);
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        winPile();
        delay(3000);
        letGo();
        
        center();
        delay(1000);
        goTo(setArray[2]);
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        winPile();
        delay(2000);
        letGo();
        
        center();
        delay(1000);
        deck();
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        goTo2(setArray[0]);
        delay(2000);
        letGo();
        delay(1000);
        
        center();
        delay(1000);
        deck();
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        goTo2(setArray[1]);
        delay(2000);
        letGo();
        delay(1000);
        
        center();
        delay(1000);
        deck();
        delay(3000);
        pickUp();
        delay(2000);
        center();
        delay(1000);
        goTo2(setArray[2]);
        delay(3000);
        letGo();
        delay(1000);        
        
        fullString = "";
        setPos = "";
        
        homePosition();
        
        Serial.write("pic\n");
        
    }else{
        relax(); 
    }
}
  
void goTo(int pos){
       
     if(pos == 10){
       pos1(236,555, 535, 190);
     }else if(pos == 5){
       pos1(208, 562, 560,200);
     }else if(pos == 0){
       pos1(170, 560, 560,202);
     }else if(pos == 11){
       pos1(246, 638, 695, 273);
     }else if(pos == 6){
       pos1(205, 644, 728, 300);
     }else if(pos == 1){
       pos1(165, 634, 706, 289);
     }else if(pos == 12){
       pos1(246, 679, 794, 320);
     }else if(pos == 7){
       pos1(200, 690, 808, 327);
     }else if(pos == 2){
       pos1(152, 682, 792, 313);
     }else if(pos == 13){
       pos1(250, 710, 855, 340);
     }else if(pos == 8){
       pos1(198,726, 886, 375);
     }else if(pos == 3){
       pos1(134, 721, 869, 362);
     }else if(pos == 14){
       pos1(260, 756, 925, 375);
     }else if(pos == 9){
       pos1(190,750, 935, 360);
     }else if(pos == 4){
       pos1(116, 755, 915, 371);
     }
 }
 
void goTo2(int pos){
       
     if(pos == 10){
       pos2(236,555, 535, 190);
     }else if(pos == 5){
       pos2(208, 562, 560,200);
     }else if(pos == 0){
       pos2(170, 560, 560,202);
     }else if(pos == 11){
       pos2(246, 638, 695, 273);
     }else if(pos == 6){
       pos2(205, 644, 728, 300);
     }else if(pos == 1){
       pos2(165, 634, 706, 289);
     }else if(pos == 12){
       pos2(246, 679, 794, 320);
     }else if(pos == 7){
       pos2(200, 690, 808, 327);
     }else if(pos == 2){
       pos2(152, 682, 792, 313);
     }else if(pos == 13){
       pos2(250, 710, 855, 340);
     }else if(pos == 8){
       pos2(198,726, 886, 375);
     }else if(pos == 3){
       pos2(134, 721, 869, 362);
     }else if(pos == 14){
       pos2(260, 756, 925, 375);
     }else if(pos == 9){
       pos2(190,750, 935, 360);
     }else if(pos == 4){
       pos2(116, 755, 915, 371);
     }
 }
 
void pos1(int servo2, int servo1, int servo4, int servo5){
    //move each servo to correct postiton
       SetSpeed(60);
       SetPosition(1,770);
       delay(500);
       SetPosition(4,730);
       delay(2000);
       SetSpeed(40);
       SetPosition(2,servo2);
       SetPosition(4,servo4);
       SetPosition(5,servo5);
       SetPosition(1,servo1 + 75);
       delay(3000);
       SetPosition(1,servo1-10);
       delay(1000);
}

void pos2(int servo2, int servo1, int servo4, int servo5){
    //move each servo to correct postiton
       SetSpeed(60);
       SetPosition(1,770);
       delay(500);
       SetPosition(4,730);
       delay(2000);
       SetSpeed(40);
       SetPosition(2,servo2);
       SetPosition(4,servo4);
       SetPosition(5,servo5);
       SetPosition(1,servo1 + 75);
       delay(3000);
       SetPosition(1,servo1+10);
       delay(1000);
}

void homePosition(){
    //move each servo to correct postiton
    pos1(187, 948, 920, 243);
}

void winPile(){
    //move each servo to correct postiton
    pos1(260, 846, 924, 254);
}

void deck(){
    //move each servo to correct postiton
    pos1(23,722,885,368);
}

void center(){
  pos1(194,759,730,174);
}

void pickUp(){
    //starts pump
    digitalWrite(1, HIGH);
}

void letGo(){
    //reverse pump
    digitalWrite(1, LOW);
}

void torqueOn(){
    //turn torque on
    TorqueOn(1);
    TorqueOn(2);
    TorqueOn(4);
    TorqueOn(5);
}

void relax(){
    //turn torque off
    Relax(1);
    Relax(2);
    Relax(4);
    Relax(5);
    
}

void SetSpeed(int speedVal){
  ax12SetRegister2(1, AX_GOAL_SPEED_L, speedVal);
  ax12SetRegister2(2, AX_GOAL_SPEED_L, speedVal);
  ax12SetRegister2(4, AX_GOAL_SPEED_L, speedVal);
  ax12SetRegister2(5, AX_GOAL_SPEED_L, speedVal);
}

void SetCompliancewMargin(int margin){
  ax12SetRegister2(1, AX_CW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(2, AX_CW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(4, AX_CW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(5, AX_CW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(1, AX_CCW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(2, AX_CCW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(4, AX_CCW_COMPLIANCE_MARGIN, margin);
  ax12SetRegister2(5, AX_CCW_COMPLIANCE_MARGIN, margin);
}

