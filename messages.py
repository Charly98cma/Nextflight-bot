# String with all the commands
commands_msg = "<b>Commands to control me:</b>\n" +\
        "/start - Start the conversation with me\n" +\
        "/help - Display the list of commands\n" +\
        "/next - Information about next lauch\n" +\
        "/cancel - Ends the conversation"


# Start message with all the commands
welcome_msg = "Hello there!\n\n" +\
    "I can help you keep track of the next rocket launch, you just need to ask :D\n\n" + commands_msg


# Message asking for location
location_msg = "But first, send me <b>your location</b> please, it's only used to give you the dates and times on your timezone.\n" +\
    "Use <b>/skip</b> if you dont want to give me your location."


# Message if user doesnt give location
skip_location_msg = "Okey, dates and times will be <b>UTC</b> from now on."


# User send text that doesnt correspond with a command
unknown_msg = "Sorry, I didn't understand that command."


# Cancel message when conversation ends
cancel_msg = "Bye! Hope we talk again soon :D"
