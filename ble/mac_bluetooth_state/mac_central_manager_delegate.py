from Cocoa import NSObject
from CoreBluetooth import CBManagerStatePoweredOn, CBManagerStatePoweredOff
import objc


class CentralManagerDelegate(NSObject):
    def init(self):
        self = objc.super(CentralManagerDelegate, self).init()
        if self is None:
            return None
        self.callback = None
        return self

    def set_callback(self, callback):
        self.callback = callback

    def centralManagerDidUpdateState_(self, central):
        state = central.state()
        if state == CBManagerStatePoweredOn:
            state_str = "Bluetooth is powered on"
        elif state == CBManagerStatePoweredOff:
            state_str = "Bluetooth is powered off"
        else:
            state_str = f"Bluetooth state changed to: {state}"
        if self.callback:
            self.callback(state_str)
