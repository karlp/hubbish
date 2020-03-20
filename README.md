## Hubbish is not rubbish.

Hubbish is a USB 2.0 HS hub.  And?  It has per port power switching and overrcurrent shutoff.
And? It is designed for cascading, with 6 ports for user devices on the front, and ports
on each side for directly plugging together.  And? That's it.

## but why.gif?

Per port power switching was a goal.  Also, "this should be really simple!"
Also, to make the physical layout sensible for the desired use case.  Initially, this
project was conceived to be part of regression testing the USB stack for
[libopencm3](http://www.libopencm3.org).  The _minimal_ test setup there required 17
USB devices.  This is also why the ports are paired.  It's setup to have one port
for the DUT and one for the test driver.  They are otherwise completely independent.

That's all folks!

## Design goals
Cheap as shit, but fully functional. So, cheapest china compatible parts for everything,
but to avoid running into hub depth limits, and make config simpler, still using a
7 port hub, not attempting to cascade 4 port hubs.  Given that the original design goal requires
3 stacked hubs for 18 test ports, caascading hubs internally was not appealing.

Still, doing usb-hs on 2 layers requires fat traces and isolation to do properly, so this
setup is currently targetting jlcpcb's cheap as shit 4 layer 2313 stackup.

Oh, and design it to actually go in a case.

## Origins
This project was split out from the [libopencm3-tests](http://github.com/karlp/libopencm3-tests)
repository when it became apparent that it was it's own monster.
