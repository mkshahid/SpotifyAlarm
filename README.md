# SpotifyAlarm
Welcome! This tool allows you to link your Spotify account and create an alarm. 

Let's start off with some back story! I used to be notorious for setting alarms for all of my tasks, and for each alarm, I would use one of iPhone's annoying default ringtones. After receiving several complaints from friends and family, who would suffer through me setting and snoozing these alarms over and over, I decided to switch my ringtone to one of my favorite songs at the time. However, I quickly learned that "solution" would only last a few days before my friends and I would start to get sick of that song and associate it with having to perform a task. This problem was the source of my idea: if I could create an alarm that played a different song as its ringtone, I could avoid annoying my peers and continue loving each song I played.

In short, instead of having to listen to the same, annoying default ringtones, this tool allows you to either select a random playlist or create a playlist with your recent favorite songs (similar to Spotify Wrapped). Based on your selection, a random song from the playlist you selected is played to whichever device you'd like (besides your mobile phone) at the time and day of week you set. A website that's hosted using Heroku with basic React front-end and a Python Flask backend is used to allow users to link their Spotify accounts and set up the alarms. 

Although I built the tool with this specific mission in mind, I actually benefitted from using it in other ways. I noticed that I became more motivated to start my day, given the fact that I could wake up to some of my recent favorite songs. I also began to snooze my alarms much less frequently, which allowed me to maximize my efficiency (and annoy my friends a bit less).

Overall, I'm very pleased with the results. Unfortunately, I've had to take down the website due to restrictions with Amazon Firebase (which I used to store login information to speed up the sign-in process for a returning user) and Python Anywhere (which I used to create the triggers to start the playback of the songs and auto generate the "Recent Favorites" playlists).

The login GitHub repo can be found here: https://github.com/mkshahid/SpotifyAlarmLogin
