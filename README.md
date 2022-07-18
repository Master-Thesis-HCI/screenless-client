# screenless-client

Developed for Raspberry Pi with NeoPixel LED strip.

1. Pulls frame data from screenless-server.
2. Saves frame to file.
3. Displays frame using NeoPixel.

Run each 5 minutes using crontab:  
`*/5 * * * *	/path/to/frame.py TOKEN`

The AIS forgets it's state after the physical power switch has been toggled. The file `ensure_frame.py` should be ran as a seperate continuous service (e.g. systemd) to automatically set the LEDs back to their last saved state after they've temporarily powered down.
