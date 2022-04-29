//write
//for com nop
//esperar 1/9600
//1clock 1/ 21.10^6
//write
//for com nop

//para high impar
//stop


void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT);    // sets the digital pin 8 as output
}

// 01100001
void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
  digitalWrite(8, LOW);
  _sw_uart_wait_T();
  digitalWrite(8,HIGH);
  _sw_uart_wait_T();
  digitalWrite(8,LOW);
  _sw_uart_wait_T();
  digitalWrite(8,LOW);
  _sw_uart_wait_T();
  digitalWrite(8,LOW);
  _sw_uart_wait_T();
  digitalWrite(8,LOW);
  _sw_uart_wait_T();
  digitalWrite(8,HIGH);
  _sw_uart_wait_T();
  digitalWrite(8,HIGH);
  _sw_uart_wait_T();
  digitalWrite(8,LOW);
  _sw_uart_wait_T();
  digitalWrite(8,HIGH);
  _sw_uart_wait_T();
  digitalWrite(8,HIGH);
  _sw_uart_wait_T();
}


// MCK 21MHz
void _sw_uart_wait_T() {
  for(int i = 0; i < 2187; i++)
    asm("NOP");
}
