# Makefile for LEGO SPIKE (Pybricks) workflow
# --------------------------------------------
# Targets:
#   make flash              # flash Pybricks firmware (hub name = $USER)
#   make run                # run main.py via BLE
#   make run FILE=foo.py    # run foo.py via BLE
#   make lego               # open web tool to restore official LEGO firmware
#   make fetch-firmware     # (optional) download a specific Pybricks firmware ZIP
#   make dfu-hint           # how to enter DFU mode

PYBRICKSDEV    ?= pybricksdev
BLE_NAME       ?= $(USER)
PY_FILE        := $(if $(FILE),$(FILE),main.py)

# Choose the exact firmware asset you want to use and its URL.
# You may update these to the latest release from
# https://github.com/pybricks/pybricks-micropython/releases
FIRMWARE_ZIP   ?= pybricks-primehub-v3.6.1.zip
FIRMWARE_URL   ?= https://github.com/pybricks/pybricks-micropython/releases/download/v3.6.1/pybricks-primehub-v3.6.1.zip

# Detect DFU device (LEGO vendor:product 0694:0008)
DFU_OK := $(shell lsusb | grep -q "0694:0008" && echo yes || echo no)


flash: $(FIRMWARE_ZIP)
	@if [ "$(DFU_OK)" != "yes" ]; then \
	  echo "⚠️  No DFU device detected."; \
	  echo "    Turn off the hub completely,"; \
	  echo "    then hold the center button while connecting it via USB:" \
	  echo "       	orange blinking LED = DFU mode."; \
	  echo "    After that, run: make flash"; \
	  exit 1; \
	fi
	@echo "🚀 Flashing Pybricks firmware (hub name: '$(BLE_NAME)') ..."
	$(PYBRICKSDEV) flash --name "$(BLE_NAME)" "$(FIRMWARE_ZIP)"

run:
	@echo "▶️  Running $(PY_FILE) on hub '$(BLE_NAME)' via BLE ..."
	$(PYBRICKSDEV) run ble --name "$(BLE_NAME)" $(PY_FILE)

lego:
	@echo "🧱 Opening the web tool to restore the official LEGO firmware ..."
	@open "https://code.pybricks.com/"

fetch-firmware:
	@if command -v curl >/dev/null 2>&1; then \
	  echo "⬇️  Downloading firmware from $(FIRMWARE_URL) ..."; \
	  curl -L -o "$(FIRMWARE_ZIP)" "$(FIRMWARE_URL)"; \
	elif command -v wget >/dev/null 2>&1; then \
	  echo "⬇️  Downloading firmware from $(FIRMWARE_URL) ..."; \
	  wget -O "$(FIRMWARE_ZIP)" "$(FIRMWARE_URL)"; \
	else \
	  echo "❌ Neither curl nor wget found. Please download the ZIP manually:"; \
	  echo "   $(FIRMWARE_URL)"; \
	  exit 1; \
	fi

dfu-hint:
	@echo "DFU mode steps:"
	@echo "1) Turn the hub off (hold center button ~5s)."
	@echo "2) Hold the center button and connect via USB."
	@echo "3) Release when the light bar blinks orange."
	@echo "Then run: make flash"

.PHONY: flash run lego fetch-firmware dfu-hint
