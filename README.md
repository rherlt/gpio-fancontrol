# README

to automatically run the application on Raspian at user login, what currently automatically happens at startup, checkout all files to home directory and add the following line to ```~/.bashrc```

```bash
#start fan speed controller
~/gpio-fancontrol/fancontrol.sh start
```

# Credits
Some code and ideas taken from Nathan.OTN, thank you very much: https://forum.libreelec.tv/thread/29050-rpi4-le12-0-1-autostart-sh-with-python-script-for-fan-control-won-t-work/?postID=195360#post195360