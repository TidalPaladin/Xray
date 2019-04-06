# RF Control

The first iteration of my X-ray controller used a 433 MHz wall outlet
for beam control. A Raspberry Pi served as the central hub for image
capture, running the scripts contained here to control:

1. A DSLR via a USB cable and `gphoto2`
2. The beam source via a 433 MHz transmitter

This approach is no longer used. A key limitation was the inability to
confirm if a beam control signal had been received, as the RF outlet
had no means of acknowledging receipt of a signal. The X-ray source can
suffer heat damage if the beam is left on for more than a few seconds,
and so an alternate method of control was explored. This control
scheme uses a Sonoff smart relay and can be found in the appropriately
named folder in the root of this repository.

The code used here would benefit from refactoring if it is to be used,
as it was written much earlier in my journey as a programmer.
