# mousetrap_monitoring
A simple Python script for monitoring mouse traps using a Raspberry Pi using gpiozero (https://github.com/gpiozero/gpiozero/)

Simply connect one wire to ground and one wire to a GPIO-pin, set those pins in the code and lightly connect the wires at the mouse trap so that when it triggers the wires are disconnected. Or use some fancier method like perhaps IR break beam sensors or magnet connectors or something. I kept it very simple.

I also use Pushover for push notifications.
