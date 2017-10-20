import os

TOKEN = '465434046:AAHZLWGbW2WfCmx1AWi6sfjOMm_tNVrMkW4'
PORT = int(os.environ.get('PORT', '5000'))
updater = Updater(TOKEN)
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://meteokavgr.herokuapp.com/" + TOKEN)
updater.idle()
