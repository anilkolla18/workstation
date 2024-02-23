# APICOPS

  # apicops to get content from Tables

  ```
  apicops tables:get-contents apim.webhook -n {namespace} -e > webhook.txt
  apicops tables:get-contents apim.gateway_service -n {namespace} > gateway_service.txt
  apicops tables:get-contents apim. configured gateway service -n {namespace) -e > configured_gateway_service.txt
  ```
# Toolkit

# Manager
# Portal
# Analytics
# Gateway


# How to shutdown or restart IBM DataPower Appliance

Purpose:
Shutdown or restart DataPower appliance.

Before we go to shutdown or restart procedure let's learn shutdown parameters which are needed during shutdown or restart of DataPower Appliance.

Shutdown DataPower parameters:
1. Reboot
    It will shutdown and restart the appliance.
2. Reload
    It will restart the appliance.
3. Halt
    It will shutdown the appliance.
4. Seconds
    Specifies the number of seconds delay before the appliance starts the shutdown operation.

Shutdown or restart using GUI/Console:
1. Login to DataPower WebGui
2. Under default domain go to Administration => Main => System Control
3. Scroll Down and go to Shutdown section
4. Select mode(e.g. Reboot System) and Delay (e.g. 10 Secs)
5. Click on Shutdown

Shutdown or restart using CLI:
1. Login to DataPower host
2. Go to default domain
3. Execute command
    ```
    shutdown reboot 10
    ```
   After 10 secs it will shutdown and reboot datapower appliance.
5. To reload use,
    ```
    shutdown reload 30
    ```
    To halt use,
    ```
    shutdown halt 30
    ```
