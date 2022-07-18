from machine import Pin, Timer
from time import sleep_ms
import ubluetooth

class BLE():


    def __init__(self, name="ESP32", led=2):
        
        self.name = name
        self.ble = ubluetooth.BLE(self.name)
        self.ble.active(True)

        self.led = Pin(led, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        self.message = bytearray()
        self.flag = False
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()


    def connected(self):
        
        self.timer1.deinit()
        self.timer2.deinit()


    def disconnected(self):
        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0))
    

    def ble_irq(self, event, data):

        if event == 1:
            '''Central connected'''
            self.connected()
            self.led(1)
        
        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()
        
        elif event == 3:
            '''New message received'''
            self.flag = True
            self.receive()
            
    def register(self):
        
        # Nordic UART Service
        UUID_Service = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        UUID_RX = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        UUID_TX = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'
            
        BLE_Service = ubluetooth.UUID(UUID_Service)
        BLE_RX = (ubluetooth.UUID(UUID_RX), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(UUID_TX), ubluetooth.FLAG_NOTIFY)
            
        BLE_UART = (BLE_Service, (BLE_TX, BLE_RX,))
        SERVICES = (BLE_UART, )
        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(SERVICES)


    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '\n')

    
    def receive(self):
        self.message = self.ble.gatts_read(self.rx)


    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytearray('\x02\x01\x06') + bytearray((len(name) + 1, 0x09)) + name)
        
# test
def demo():
    ble = BLE()

if __name__ == "__main__":
    demo()