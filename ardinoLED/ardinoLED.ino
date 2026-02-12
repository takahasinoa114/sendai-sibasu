#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define DEVICES_NUM 4

const int PIN_CS = 1;
const int PIN_SCK = 2;
const int PIN_MOSI = 3;

MD_MAX72XX LED = MD_MAX72XX(HARDWARE_TYPE, PIN_CS, DEVICES_NUM);

void setup() {
  //SPIの初期設定
  SPI.setCS(PIN_CS);
  SPI.setSCK(PIN_SCK);
  SPI.setTX(PIN_MOSI);
  SPI.begin();

  //LEDマトリクスの制御開始
  LED.begin();
  //明るさの調整(1～15)
  LED.control(MD_MAX72XX::INTENSITY, 3);
  //setPointをするたびに表示を更新
  LED.update(MD_MAX72XX::ON);
}

void loop() {
  //点滅
  LED.setPoint(0, 0, 1);
  delay(1000);
  LED.setPoint(0, 0, 0);
  delay(1000);

  //座標の確認
  LED.setPoint(7, 0, 1);
  delay(1000);
  LED.setPoint(0, 7, 1);
  delay(1000);
  LED.setPoint(0, 8, 1);
  delay(1000);
  LED.setPoint(0, 16, 1);
  delay(1000);
  LED.setPoint(0, 24, 1);
  delay(1000);

  //全て消灯
  LED.clear();
}