"""Constants for Aquafeast Water Leak integration."""

DOMAIN = "aquafeast_water_leak"
DEFAULT_NAME = "Aquafeast Water Leak Sensor"

# Configuration
CONF_DEVICE_ID = "device_id"          # ако ще се ползва (не е задължително)
CONF_MAC = "mac_address"
CONF_DEVICE_MODEL = "device_model"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_DEVICE_MODEL = "BSK_BR"
DEFAULT_SCAN_INTERVAL = 30

# API
BASE_URL = "https://interface.briskworld.com"    # използвай HTTPS
GET_STATE_URL = f"{BASE_URL}/devSta/getState/app"
CONTROL_URL = f"{BASE_URL}/device/control/app"

# Data keys (от API отговора)
KEY_VALVE = "data01"          # 0 = затворен (сухо), 1 = отворен (теч)
KEY_PROTECTION_MODE = "data02"
