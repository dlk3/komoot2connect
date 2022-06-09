# Komoot2Connect

A script to copy completed tours from my Komoot account to my Garmin Connect account.

Instructions:

1) Create a <code>~/.config/k2c.cfg</code> file containing the login credentials for each site.  See the sample file in this repository for the format.
2) Run the <code>k2c</code> script

WARNING: Be sure that the "Automatically pull completed Tours from Garmin" option is turned off in Komoot connection settings, otherwise you'll end up with duplicate activities in Komoot.  It is ok to leave "Automatically push planned Tours to Garmin" turned on however.
