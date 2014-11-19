Elster
======

Elster's (and other elster based products) communication library. Works with Stiebel Eltron's WPW. 

Work here is based on Juergs work (http://juerg5524.ch/list_data.php), peeking into comfort soft application and many hours of trying.

The heatpump has 2 intefaces: IR and CAN. This library communicates through CAN interface using "some" ethernet->can bridge. Right now there are 2 existing bridge types that are supported:
- juerg's r-pi with can cape and can_server from his can_progs archive
- embedded stm32 based board (with lwip stack) (sources will be added later)

With some minimal work it should be able to adapt the interface to IR. I'll leave that as exercise to some one else ;)

So far there are few programs available:
- discovery - discovers available devices on bus
- scan - discovers devices, and does scan of all possible variables
- get - retrieves variables from devices on bus, and submits them to the "volkszahler" instalation
- listen - listens on bus, decodes and prints all messages seen
- simulation - tries to simulate device on the bus (not working properly yet)

For each program to work you need:
- setup the bridge and can connection properly
- know the IP address of the bridge
- edit the desired program, and rewrite the IP address
- execute

Warranty is as always - none. You are responsible for destroying your own stuff and dying in cold this winter. ;)


