#! /bin/sh

# Make sure to update the {user} value in the plist file
# Make sure to "chmod +x textbundler.sh"

cp textbundler.sh ~/
cp com.textbundler.agent.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.textbundler.agent.plist
