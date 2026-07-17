from devices.power_supplies.owon_spe3051 import OwonSPE3051
from devices.power_supplies.manager import PowerSupplyManager

from core.device_manager import DeviceManager

# psu = OwonSPE3051()
# print("ID:", psu.id)
# print("Name:", psu.name)

# # conectează cu portul tău (de ex. "usb0", "COM3", etc.)
# psu.connect("COM12")

# print("Connected:", psu.is_connected())
# print("Voltage:", psu.measure_voltage())
# print("Current:", psu.measure_current())





# manager = PowerSupplyManager()
# available = manager.get_available()
# print(available)






dm = DeviceManager()
while True:
    for ps in dm.power_supplies.power_supplies.values():
        print(f" connected: {ps.is_connected}")

    available = dm.power_supplies.get_available()
    print(available)






# from devices.power_supplies.owon_spe3051 import OwonSPE3051

# print("=== Test scanare COM 1-20 ===")

# for i in range(1, 300):
#     com = f"COM{i}"
#     try:
#         psu = OwonSPE3051()
#         psu.connect(com)
#         print(f"✓ Connected to {com}, is_connected: {psu.is_connected()}")
#         break
#     except Exception as e:
#         print(f"✗ {com}: {type(e).__name__}")

# print("=== Test terminat ===")