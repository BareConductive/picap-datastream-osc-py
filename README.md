[![Bare Conductive](http://bareconductive.com/assets/images/LOGO_256x106.png)](http://www.bareconductive.com/)

# Bare Conductive Pi Cap OSC Data Stream Utility

Example OSC data streaming code for the  [Bare Conductive Pi Cap](http://www.bareconductive.com/shop/pi-cap/). Streams touch and proximity data from the Pi Cap to a network target (default is 127.0.0.1) via OSC on a specified port (default is 3000). The target can be an IPv4 address or a hostname - but not an IPv6 address at this time. Can optionally interface with Bare Conductive's [MPR121 grapher](https://github.com/BareConductive/mpr121-grapher).

## Requirements

* Requires [python-dev](https://www.python.org/) (`apt-get install python-dev`)
* Requires [WiringPi](http://wiringpi.com/) (`apt-get install wiringpi`)
* Requires [Bare Conductive's MPR121 libary for WiringPi](https://github.com/BareConductive/wiringpi-mpr121)
* Requires [python-liblo](http://das.nasophon.de/pyliblo/) (`apt-get install python-liblo`)

## Install / Build

* You should install this code as part of the Pi Cap Raspbian package: `sudo apt-get install picap`    
* However, if you are doing this yourself, clone the repository and follow the usage instructions.

## Usage

    Sends Pi Cap readings through OSC - MUST be run as root.

    Usage: python datastream-osc.py [OPTION]

    Options:
      -h, --host   host address, defaults to 127.0.0.1
      -p, --port   port on which to send, defaults to 3000
          --help   displays this message

## Output message formatting

    /touch		electrode touch values (0 not touched, 1 touched)
    /tths		electrode touch thresholds (0..255)
    /rths		electrode release thresholds (0..255)
    /fdat		electrode filtered data (0..1023)
    /bval		electrode baseline values (0..1023)
    /diff		/bval - /fdat (0..1023)
