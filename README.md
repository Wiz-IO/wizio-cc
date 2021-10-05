# Texas Instruments CC26x2<br> development platform for PlatformIO

**A few words in the beginning**
* **Version: 1.1.0 ( The project is a work in progress, there may be bugs )**
* This project is based on Simplelink CC13x2_26x2 SDK 5.10.00.48 - **only driverlib**
* **[Frameworks](https://github.com/Wiz-IO/framework-wizio-cc)**
* * Arduino ( in progress... )
* * Simplelink SDK ( RTOS support TI Drivers )
* * * baremetal ( **support only driverlib** )
* * * freertos 
* * * nortos ( TODO )
* * * tirtos ( TODO )
* **Upload & Debug** ( in progress... NOT READY, use SEGGER J-FLASH for now )
* * J-LINK ( v8 )
* **ZigBee - NO OPEN SOURCE LIBRARIES**
* * TI Z-Stack ... is "full mess" - the stack support only TI-RTOS, no example source codes ... can work as super-loop(Arduino), but ... ask TI
* * FreakZ - not have Security and ZCL (tested -  **not work** with zigbee2mqtt)
* * ZBOSS 1.0 not have Security and ZCL (tested -  **not work** with zigbee2mqtt)
* * ZBOSS 3.0 - DSR want money for a license ... (tested - work with zigbee2mqtt)
* [EXAMPLES](https://github.com/Wiz-IO/examples-wizio-cc)
* [READ WIKI](https://github.com/Wiz-IO/wizio-cc/wiki)
* [Youtube Demo](https://www.youtube.com/watch?v=GS83TT35M40)

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/Arduino-CC2652.jpg)

## Install Platform
_Note: be sure [**git**](https://git-scm.com/downloads) is installed_
* PIO Home > Platforms > Advanced Installation 
* paste https://github.com/Wiz-IO/wizio-cc
* INSTALL

## Uninstall ( fast ) ... Re-Install ( do this and Install again )
* In directory C:\Users\USER_NAME\.platformio\\**platforms**
  * delete folder **wizio-cc** ( builders )
* In directory C:\Users\USER_NAME\.platformio\\**packages**
  * delete folder **framework-wizio-cc** ( sources )
  * delete folder **toolchain-gccarmnoneeabi** (compiler, **may not be deleted** )

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/PIO-CC.jpg)

![pico](https://raw.githubusercontent.com/Wiz-IO/LIB/master/images/zigbee-sensor.jpg)

## Thanks to:
* [Comet Electronics](https://www.comet.bg/en/)

***

>If you want to help / support:   
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ESUP9LCZMZTD6)
