# Bluetooth DualBoot Fixer

# Motivation

When using multiple systems on a single machine there is a problem with pairing bluetooth peripherals such as mouse 
or keyboard with all the systems at once. The solution is to copy several parameters between them.

This script handles conversion of Windows reg file to linux config file.

# Usage

1. Boot to linux
2. Clone this repo
3. Pair your device - make a note about MAC of your device 
4. Reboot to Windows
5. Pair your device
6. Open regedit as administrator
7. Navigate to `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\<BT_MAC>\<DEVICE_MAC>`
   
   Note that device MAC may differ from the one from linux.
   
   If there are no keys visible in `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys`, 
   try to add access rights for your user account.
   
8. Export the registry key to reg file
9. Reboot to linux
10. `sudo su`
11. run this script
```
python -m btfix -r regfile.reg -l /var/lib/bluetooth/<BT_MAC>/<DEVICE_MAC>/info -o <output_file>
OR
python -m btfix -r regfile.reg -l /var/lib/bluetooth/<BT_MAC>/<DEVICE_MAC>/info --inplace
```
12. Reboot to linux again (restarting bluetooth service should do it as well)
13. Your device should work now

**When using with `--inplace` option the `DEVICE_MAC` directory will be renamed to match the MAC from Windows 
and the linux config will be overwritten.**
Also a backup file will be created in `/tmp/bluetooth_backup_<current_timestamp>`.
