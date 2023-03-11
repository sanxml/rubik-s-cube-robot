#include <Servo.h>

#define MOTOR1_CP 3
#define MOTOR1_DIR 4
#define MOTOR1_EN 5
#define MOTOR2_CP 6
#define MOTOR2_DIR 7
#define MOTOR2_EN 8
#define SERVO1 10
#define SERVO2 11

#define MOTOR_PULSE 6400 //转一圈的脉冲

Servo servo_left, servo_right;
uint8_t servo_left_state[4] = {24,38,88,44};// 闭合 紧贴 张开
uint8_t servo_right_state[4] = {24,38,88,44};// 闭合 紧贴 张开  

uint8_t min_delay = 54 , max_delay = 800;

void setup()
{
//  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(MOTOR1_CP, OUTPUT);
  pinMode(MOTOR1_DIR, OUTPUT);
  pinMode(MOTOR1_EN, OUTPUT);
  pinMode(MOTOR2_CP, OUTPUT);

  pinMode(MOTOR2_DIR, OUTPUT);
  pinMode(MOTOR2_EN, OUTPUT);
  digitalWrite(MOTOR1_DIR, HIGH);
  digitalWrite(MOTOR1_EN, LOW);
  digitalWrite(MOTOR2_DIR, HIGH);
  digitalWrite(MOTOR2_EN, LOW);

  Serial.begin(115200); //打开串口

  servo_left.attach(SERVO1,500,2500);
  servo_right.attach(SERVO2,500,2500);

  servo_left.write(servo_left_state[3]);
  servo_right.write(servo_right_state[3]);
  delay(200);

//  servo_left.write(servo_left_state[0]);
//  delay(500);
//  servo_right.write(servo_right_state[2]);
//  delay(3000);
//  servo_left.write(servo_left_state[3]);
//  servo_right.write(servo_right_state[3]);
//  delay(3000);
//  servo_left.write(servo_left_state[2]);
//  servo_right.write(servo_right_state[0]);
//  delay(3000);
}

void loop(){

  String buf = "";
  while (Serial.available() == 0);
  while (Serial.available() > 0){
      buf += char(Serial.read());
      delay(5);
  }
  
  if(buf.length()>=65){
    Serial.flush();
    while (Serial.available() == 0);
    while (Serial.available() > 0){
      buf += char(Serial.read());
      delay(5);
    }
  }
  //Serial.print(buf.length());
  motor_solution(buf);
  Serial.println(buf);
  Serial.flush();

} 

//L2 D2 R' F2 D2 F2 U2 L' B2 D2 L' F' D' L U2 R D F' U L
//rzrzRRzRzFZZrZZxfxFXXrZRzRzrZFFzRZRRFFxfxFFXXZZRRZrzRR
//R' D' L2 U F L' U' B R' U R D' F2 D R2 F2 U' B2 L2 D' L2
//L2 D L2 B2 U F2 R2 D' F2 D R' U' R B' U L F' U' L2 D R

void motor_solution(String cube_list){
  uint8_t i = 0;
  for(; i<cube_list.length(); i++){
    // Serial.print(cube_list[i]);
    if(cube_list[i] == 'S'){
      uint8_t cube_speed = (uint8_t)cube_list[i+1]*10 + (uint8_t)cube_list[i+2] - 16;
      Serial.print("Speed = ");
      Serial.println(cube_speed);
      min_delay = cube_speed;
      cube_list = ' ';
   }
    char temp = cube_list[i];
    if (temp == cube_list[i+1]){
      cube_list[i+1] = '2';
      i++;
    }
  }
  // Serial.println(cube_list);
  uint8_t left_motor_flag = 0, right_motor_flag = 0;
  for(i=0; i<cube_list.length(); i++){
    int8_t left_round, right_round;
    if(cube_list[i] == 'r' || cube_list[i] == 'f' || cube_list[i] == 'x' || cube_list[i] == 'z')
      left_round = right_round = -1;
    else
      left_round = right_round = 1;

    if(cube_list[i+1] == '2'){
      if(left_motor_flag == 0)
        left_round = 2;
      else
        left_round = -2;
      if(right_motor_flag == 0)
        right_round = 2;
      else
        right_round = -2;
    }
    if(cube_list[i] == 'r'){
      cube2motor('R', right_round);
//      Serial.println('r');
      if(cube_list[i+1] == '2')
        right_motor_flag = !right_motor_flag;
    }
    else if(cube_list[i] == 'f'){
      cube2motor('F', left_round);
//      Serial.println('f');
      if(cube_list[i+1] == '2')
        left_motor_flag = !left_motor_flag;
    }
    else if(cube_list[i] == 'x'){
      cube2motor('X', right_round);
//      Serial.println('x');
      if(cube_list[i+1] == '2')
        right_motor_flag = !right_motor_flag;
    }
    else if(cube_list[i] == 'z'){
      cube2motor('Z', left_round);
//      Serial.println('z');
      if(cube_list[i+1] == '2')
        left_motor_flag = !left_motor_flag;
    }
    else if(cube_list[i] == 'R' || cube_list[i] == 'X')
    {
      cube2motor(cube_list[i], right_round);
//      Serial.println(cube_list[i]);
      if(cube_list[i+1] == '2')
        right_motor_flag = !right_motor_flag;
    }
    else if(cube_list[i] == 'F' || cube_list[i] == 'Z')
    {
      cube2motor(cube_list[i], left_round);
//      Serial.println(cube_list[i]);
      if(cube_list[i+1] == '2')
        left_motor_flag = !left_motor_flag;
    }
    else if(cube_list[i] == 'C'){
      cube2motor('C', right_round);
//      Serial.println('C');
    }
    else if(cube_list[i] == 'c'){
      servo_left.write(servo_left_state[3]);
      servo_right.write(servo_right_state[3]);
//      Serial.println('c');
    }
    else if(cube_list[i] == 'l'){
      servo_left.write(servo_left_state[0]);
      servo_right.write(servo_right_state[0]);
//      Serial.println('l');
    }
    if(cube_list[i+1] == '2'){
      i++;
//      Serial.println('2');
    }
  }
}

void cube2motor(char cube_list, int8_t round){
  servo_left.write(servo_left_state[0]);
  servo_right.write(servo_right_state[0]);
  delay(80);
  if(cube_list == 'R'){
    servo_right.write(servo_right_state[1]);
    motor_turning('R', round);
    if(round == 1 || round == -1){
      servo_right.write(servo_right_state[2]);
      delay(100);
      motor_turning('R', -round);
    }
  }
  else if(cube_list == 'F'){
    servo_left.write(servo_left_state[1]);
    motor_turning('L', round);
    if(round == 1 || round == -1){
      servo_left.write(servo_left_state[2]);
      delay(100);
      motor_turning('L', -round);
    }
  }
  else if(cube_list == 'X'){

    if(round == 1 || round == -1){
      servo_right.write(servo_right_state[2]);
      delay(100);
      motor_turning('R', -round);
      servo_right.write(servo_right_state[0]);
      delay(80);
      servo_left.write(servo_left_state[2]);
      delay(100);
      motor_turning('R', round);
    }
    else{
      servo_left.write(servo_left_state[2]);
      delay(100);
      motor_turning('R', round);
      servo_left.write(servo_left_state[3]);
      delay(80);
      servo_right.write(servo_right_state[3]);
      delay(100);
    }

  }
  else if(cube_list == 'Z'){
    if(round == 1 || round == -1){
      servo_left.write(servo_left_state[2]);
      delay(100);
      motor_turning('L', -round);
      servo_left.write(servo_left_state[0]);
      delay(80);
      servo_right.write(servo_right_state[2]);
      delay(100);
      motor_turning('L', round);
    }
    else{
      servo_right.write(servo_right_state[2]);
      delay(100);
      motor_turning('L', round);
      servo_right.write(servo_right_state[3]);
      delay(80);
      servo_left.write(servo_left_state[3]);
      delay(100);
    }
  }
  if(cube_list == 'C'){
      servo_right.write(servo_right_state[3]);
      servo_left.write(servo_left_state[3]);
      delay(200);
      servo_right.write(servo_right_state[0]);
      servo_left.write(servo_left_state[0]);
  }
    
    servo_right.write(servo_right_state[0]);
    servo_left.write(servo_left_state[0]);
    delay(120);
    servo_right.write(servo_right_state[1]);
    servo_left.write(servo_left_state[1]);
    delay(50);
}

void motor_turning(char motor, float right_angle){
  uint8_t cp_pin = 0 , dir_pin = 0;
  if(motor == 'L'){
    cp_pin = MOTOR1_CP;
    dir_pin = MOTOR1_DIR;
  }
  else if(motor == 'R'){
    cp_pin = MOTOR2_CP;
    dir_pin = MOTOR2_DIR;
  }
  if(right_angle >= 0){
    digitalWrite(dir_pin, HIGH);
    motor_pulse(cp_pin, (int)(right_angle*MOTOR_PULSE/4));
    // Serial.println(right_angle*MOTOR_PULSE/4);
  }
  else if(right_angle < 0){
    digitalWrite(dir_pin, LOW);
    motor_pulse(cp_pin, -(int)(right_angle*MOTOR_PULSE/4));
  }
}

void motor_pulse(uint8_t pin, uint16_t num){
  // Serial.println(num);
  uint16_t num_init = num;
  uint8_t delay_time = 0 ;
//  for(; num>num_init/3*2; num--){
//    delay_time = map(num,num_init,num_init/3*2,max_delay,min_delay);
//    // Serial.println(delay_time);
//    digitalWrite(pin, HIGH);
//    delayMicroseconds(delay_time);
//    digitalWrite(pin, LOW);
//    delayMicroseconds(delay_time);
//  }
//  for(; num>num_init/3; num--){
//    // Serial.println(min_delay);
//    digitalWrite(pin, HIGH);
//    delayMicroseconds(min_delay);
//    digitalWrite(pin, LOW);
//    delayMicroseconds(min_delay);
//  }
//  for(; num>0; num--){
//    delay_time = map(num,num_init/3,0,min_delay,max_delay);
//    // Serial.println(delay_time);
//    digitalWrite(pin, HIGH);
//    delayMicroseconds(delay_time);
//    digitalWrite(pin, LOW);
//    delayMicroseconds(delay_time);
//  }

  for(; num>0; num--){
    digitalWrite(pin, HIGH);
    delayMicroseconds(min_delay);
    digitalWrite(pin, LOW);
    delayMicroseconds(min_delay);
  }
}
