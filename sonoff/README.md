# Sonoff Control

This approach to beam control uses a Sonoff smart relay to toggle
power to the beam. Furthermore, the need for a Raspberry Pi as a
centralized point of control is eliminated. In this implementation,
the Sonoff controls the DSLR shutter through Nikon's remote shutter
interface. While this ensures that the beam will not be left on for
more than a safe window of time, the ability to control the DSLR at a
high level through `gphoto2` is lost.

If I were to resume development of this control software, my approach
would likely be to forego the Sonoff and use a Raspberry Pi as a
single point of control, where the beam would be toggled directly
through the Raspberry Pi's GPIO interface. With access to a 3D printer
it would be possible to cleanly wire up the X-ray head without exposed
mains connections. I would then implement an additional hardware
safeguard to ensure that unexpected behavior in software could not
leave the beam in an unsafe state.
