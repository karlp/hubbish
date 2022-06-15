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


## Tools
The project uses kicad 5.99 era project files, sorry about that.

## Versions
### "r2" r2021-03  (lol, finished and ordered 2022-06)
### Improvements:
Adds a 30-40ish Watt power supply.  Inductor is rated to 9A, regulator to 12A. Per port power switches are
still 1A nominal, so nominally 7x5x1 = 35W for the ports plus around .5x3.3 for the hub itself, or an extra say 2W.

Resizes to 100x80mm so cheaper manufacturing again.  We're no longer trying to find an off the shelf case.
Places like 3d craft cloud have gotten so cheap I'm going to just make a custom case and have it printed on demand.

What's it look like?
![r2022-06 board view](r2021-02/hubbish-rev2-202206-round.png)

* [Schematic-r2](r2021-02/hubbish-rev2.pdf)

#### Bugs
Lol none!  (ordered only so far, not assembled yet.
vertical z-axis has been skipped for this one so far...


### r2020-03
What's it look like?
![r1 board view](r2020-03/hubbish-r1.png)
* [Schematic-r1](r2020-03/usb-test-harness.pdf)


#### Bugs

1. Missing a serial resistor for the crystal.  Doesn't enumerate the hub without it.
1. Needs a jumper wire if yout want to actually run it as a bus powered hub for testing.
1. Port numbers are super wonky.
1. .... doesn't actually work?  I suspect I just have assembly issues, but...
1. Bigger than 100x100, which fits the Bud case nicely, and didn't matter when 4L was always just size based
   but now that jlc is doing 4L super cheap for under 100x100, this can be considered a bug
1. vertical (z axis) positioning of the usptream usb-a-male and downstream usb-a-female for chaining doesn't
   align properly.


