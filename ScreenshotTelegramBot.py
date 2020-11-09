from telebot import TeleBot
from selenium import webdriver
import config

bot = TeleBot(config.TOKEN)

option = webdriver.ChromeOptions()
option.add_argument('headless')
DRIVER = "/usr/lib/chromium-browser/chromedriver"
driver = webdriver.Chrome(DRIVER, options=option)


@bot.message_handler(commands=["start"])
def welcome(message):
    """
    /start command to describe the bot to the user
    """
    bot.send_message(
        message.chat.id,
        "Hello, {0.first_name}!\n"
        "I am - <b>{1.first_name}</b>.\n"
        "Please send me link to the site the screenshot of which you would like to receive".format(
            message.from_user, bot.get_me()
        ),
        parse_mode="html",
    )


@bot.message_handler(content_types=["text"])
def conversation(message):
    """
    the function takes a link from the user takes a screenshot of the site and sends it back to the user
    """
    if message.chat.type == "private":
        try:
            driver.get(message.text)
            S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
            driver.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
            driver.find_element_by_tag_name('body').screenshot('web_screenshot.png')
            bot.send_photo(message.chat.id, open('web_screenshot.png', 'rb'))
        except:
            bot.send_message(message.chat.id, f"Wrong url, please try another one")


# Run
bot.polling(none_stop=True)
