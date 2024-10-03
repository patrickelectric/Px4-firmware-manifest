# Px4 Firmware Manifest 

> Note: This is not the official repository for PX4 parameters, no. This is just a tribute.

Before this repository, the only up-to-date representation of the board info is available inside QGC repository ([FirmwareUpgradeController.cc](\https://github.com/mavlink/qgroundcontrol/blob/780bd28a89b114083e02c87cfafcd35decddebd8/src/VehicleSetup/FirmwareUpgradeController.cc#L41)),
the same thing applies to USBBoardInfo ([USBBoardInfo.json](https://github.com/mavlink/qgroundcontrol/blob/780bd28a89b114083e02c87cfafcd35decddebd8/src/Comms/USBBoardInfo.json)).

This repository follows the same idea behind https://github.com/mavlink/qgroundcontrol/pull/10469, the structure is based on the [ArduPilot manifest format](https://firmware.ardupilot.org/manifest.json).

Files should be **updated every monday**.
