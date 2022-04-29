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
  digitalWrite(8,LOW)
  
  digitalWrite(8,HIGH)
  
  digitalWrite(8,HIGH)
  
  digitalWrite(8,LOW)
  
  digitalWrite(8,LOW)
  
  digitalWrite(8,LOW)
  
  digitalWrite(8,LOW)
  
  digitalWrite(8,HIGH)
}


// MCK 21MHz
void _sw_uart_wait_half_T(due_sw_uart *uart) {
  for(int i = 0; i < 1093; i++)
    asm("NOP");
}

void _sw_uart_wait_T(due_sw_uart *uart) {
  _sw_uart_wait_half_T(uart);
  _sw_uart_wait_half_T(uart);
}
