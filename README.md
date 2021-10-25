# screenless-client

Developed for Raspberry Pi with NeoPixel LED strip.

1. Pulls frame data from screenless-server
2. Saves frame to file
3. Displays frame using NeoPixel

Run each 5 minutes using crontab:
`*/5 * * * *	/path/to/frame.py TOKEN`

