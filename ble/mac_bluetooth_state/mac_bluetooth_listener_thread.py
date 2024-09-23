import threading
import objc
from CoreBluetooth import CBCentralManager
from Foundation import NSRunLoop, NSDate

from ble.mac_bluetooth_state.mac_central_manager_delegate import CentralManagerDelegate


class BluetoothListenerThread(threading.Thread):
    def __init__(self, on_bt_state_changed):
        super().__init__()
        self.callback = on_bt_state_changed  # Function to call when Bluetooth state changes
        self.daemon = True  # Daemonize thread to exit when main program exits

    def run(self):
        self.delegate = CentralManagerDelegate.alloc().init()
        self.delegate.set_callback(self.callback)
        self.manager = CBCentralManager.alloc().initWithDelegate_queue_(self.delegate, None)

        # Start the run loop in this thread
        self.run_loop = NSRunLoop.currentRunLoop()
        self.keep_running = True
        while self.keep_running:
            self.run_loop.runUntilDate_(NSDate.dateWithTimeIntervalSinceNow_(0.1))

    def stop(self):
        self.keep_running = False
