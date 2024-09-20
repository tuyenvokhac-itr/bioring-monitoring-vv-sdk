from Foundation import NSBundle
import objc

# Load the IOBluetooth framework
IOBluetooth = NSBundle.bundleWithIdentifier_('com.apple.Bluetooth')
functions = [("IOBluetoothPreferenceGetControllerPowerState", b'i')]
objc.loadBundleFunctions(IOBluetooth, globals(), functions)


def check_bluetooth_state_mac_os() -> bool:
    state = IOBluetoothPreferenceGetControllerPowerState()
    if state == 1:
        return True
    else:
        return False
