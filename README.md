# Nextflight_bot
## Basic info

Hey there :D

I've made this bot to solve a problem I only had, but, hey, maybe someone else have it too, thats why I decided to make it public.

This is a pretty basic bot with the following commands:
- **/start** - Starts the conversation with the bot and this one ask for your location (only used to give dates and times according to your timezone)
- **/help**  - Gives the list of commands and a brief explanation
- **/nextflight** - Answers with the info of the next space flight (name, dates, description, location, etc..) and photo of the rocket or the infographic if it's available.
- **/nextevent** - Shows information about the next space related event (EVAs, Dock/Undock of capsules on the ISS, Press releases, etc...)
- **/cancel** - End the conversation with the bot

The bot lets you restart the conversation at any point if you want to change the timezone.

The very basics are mostly done, but I want to implement **Events** too (ISS dock/undock of capsules, EVA, etc...) and more ideas I have in mind (dates and times on user TZ, translation of texts and messages, etc...)

See the [TODO](https://github.com/Charly98cma/Nextflight-bot#todo) section to see the roadmap of this project and it's current state.

Hope you like it and it's helpful to someone else  ;)

If you want to give it a taste, once it's hosted, he's waiting you [here](https://t.me/nextflight_bot).

## Dependencies and execution
### Docker installation

There's a [Dockerfile](https://github.com/Charly98cma/Nextflight-bot/blob/master/Dockerfile) that will deploy the bot and all its dependencies on a container, making it easier to deploy and manage.

First of all, you'll need a token, see [Credentials](#credentials) for more information.

Now, you must create the docker image:
``` shell
docker build --tag nextflight-bot .
```

Now, you only have to run the image:
``` shell
docker run --detach --name nextflight-bot nextflight-bot:latest
```

And that's all! Very easy and very fast!

### Manual installation
First of all, make sure your system has already installed *Python 3* (please, stop using *Python 2* :smile: ) and *pip*.

If you don't know how to do it, [this](https://www.makeuseof.com/tag/install-pip-for-python/) article contains the commands to install it *Python 3* and *pip* on Windows, MAC, Linux (commands for each package manager) and Raspberry Pi.

This bot uses a couple of packages which are available on *pip*, see [requirements.txt](https://github.com/Charly98cma/Nextflight-bot/blob/master/requirements.txt) to see all of them.

The installation process of all the required packages has been changed to even more simple commands using the next command:

```makefile
make init
```

And... you're almost ready to take off :P

To run the bot, just execute:

```makefile
make run
```

## Credentials

To create yout bot, you must talk to the BotFather, which will guide you through the basics of setting up your bot, and will give you the token.

Once everything is set up, you have to create a new environment variable called *NF_TOKEN* with your token, which can be done executing the next command:

``` makefile
make token
```

## Acknowledgements

Thanks to the original developer of [Launch Library](https://launchlibrary.net/), the original API, and the awesome [developers](https://thespacedevs.com/about) of [The Space Devs](https://thespacedevs.com/) for improving the project and making [Launch Library 2](https://thespacedevs.com/llapi).

---

## TODO
- [x] Change description, commands and about me on BotFather
- [X] **Release first stable version**
- [x] Dates and times in user timezone, not in UTC using user location.
- [x] Bugs, fixes and typos
- [x] New **/cancel** command
- [X] Create *dev* branch and keep *master* as Stable version.
- [X] Move messages out of the main code
- [x] Add GPL License
- [x] Restructure the project to make it "professional" (unload the only .py file)
- [x] Deploy bot on VPS
- [x] Fix installation process (dependencies)
- [x] Fix **/cancel** bug (doesn't let restart the conversation)
- [x] Events (dock/undock of capsules, EVAs, etc...)
- [x] Fix `make token` that doesn't read the `token.txt` file
- [ ] Make a docker image for easy deployment
- [ ] **Release second stable version**
