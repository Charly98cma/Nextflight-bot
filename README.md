# Nextflight_bot
## Basic info

Hey there :D

I've made this bot to solve a problem I only had, but, hey, maybe someone else have it too, thats why I decided to make it public.

I'm already working on it and looking for a place to host it (maybe AWS), but at the moment, it's only working while I'm testing, but it will be ready pretty soon.

This is a pretty basic bot with the following commands:
- **/start** - Starts the conversation with the bot and this one ask for your location (only used to give dates and times according to your timezone)
- **/help**  - Gives the list of commands and a brief explanation
- **/nextflight** - Answers with the info of the next space flight (name, dates, description, location, etc..) and photo of the rocket or the infographic if it's available.
- **/cancel** - End the conversation with the bot

The very basic are mostly done, but I want to implement **Events** too (ISS dock/undock of capsules, EVA, etc...) and more ideas I have in mind (dates and times on user TZ, translation of texts and messages, etc...)

See the [TODO](https://github.com/Charly98cma/Nextflight-bot#todo) section to see the roadmap of this project, which keeps expanding almost every week.

Hope you like it and it's helpful to someone else  ;)

If you want to give it a taste, once it's released, he's wating [here](https://t.me/nextflight_bot).

## Dependencies and execution

This bot uses a couple of packages which are available on *pip*, see [requirements.txt](https://github.com/Charly98cma/Nextflight-bot/blob/master/requirements.txt) to see all of them.

All the packages can be installed by executing the next command, which gives the `requirements.txt` to *pip* and does his installation process:

```
pip install -r requirements.txt
```

And... you're almost ready to take off :P

## Credentials

To create yout bot, you must talk to the BotFather, which will guide you through the basics of setting up your bot, and will give you the token.

Once everything is set up, create a new environment variable called *NF_TOKEN* with your token, and execute the bot.

## Acknowledgements

Thanks to the original developer of [Launch Library](https://launchlibrary.net/), the original API, and the awesome [developers](https://thespacedevs.com/about) of [The Space Devs](https://thespacedevs.com/) for improving the project and making [Launch Library 2](https://thespacedevs.com/llapi).

---

## TODO
- [x] Change description, commands and about me on BotFather
- [X] **Release first stable version**
- [x] Dates and times in user timezone, not in UTC using user location.
- [x] Bugs, fixes and typos
- [x] New **/cancel** command
- [ ] Create *dev* branch and keep *master* as Stable version.
- [ ] Move messages out of the main code
- [ ] Restructure the project to make it "professional" (unload the only .py file)
- [ ] Translate texts to user language
- [ ] **Release second stable version**
- [ ] Reminder 30 mins before launch.
- [ ] Make a docker image
- [ ] ...
- [ ] Events (dock/undock of capsules, EVAs, etc...)
