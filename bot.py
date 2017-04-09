# coding=utf-8
import re

from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler

from lib import get_story, get_link_from_query

import os

hello_message = """
Здравствуй, путник

Введи ссылку на алиэкспрессе и я постараюсь сказать, как изменялась цена твоего товара
Например,
https://ru.aliexpress.com/item/seo-url/32750549213.html

Эти данные я буду нагло воровать с ресурса http://www.aliprice.com/
"""

invalid_query_text = "неверная ссылка"
empty_result_message = "поиск не сложился. Попробуйте что-нибудь другое"


def validate_query(query):
    return re.search("aliexpress", query) or is_digits(query)

def is_digits(query):
    return re.search("^\d+$", query)



def start(bot, update):
    update.message.reply_text(hello_message)


def hello(bot, update):
    update.message.reply_text(hello_message)


def inline_hello(bot, update):
    print "inline"
    print update
    results = list()
    query = update.inline_query.query

    if len(query) == 0:
        return
    message_text = invalid_query_text
    if validate_query(query):
        story = get_story(query)
        if len(story) > 0:
            message_text = ""
            if is_digits(query):
                message_text = "История изменения цен для https://ru.aliexpress.com/item/i/{}.html\n\n".format(query)
            for v in story:
                message_text += "%s\t-\t%s%s\n" % (v["date"], v["val"], v["currency"])
        else:
            message_text = empty_result_message

    results.append(InlineQueryResultArticle("1", "Цены на {}".format(query),
                                            input_message_content=InputTextMessageContent(
                                                message_text=message_text)
                                            ))

    bot.answerInlineQuery(update.inline_query.id, results, cache_time=0)


def message_handler(bot, update):
    query = update.message.text

    link = get_link_from_query(query)

    if validate_query(link):
        update.message.reply_text("Подождите...")
        print("get_story %s" % link)
        story = get_story(link)
        print("story result %s" % story)

        if len(story) > 0:
            update.message.reply_text("Кажется, что-то есть:")

            msg = ""
            for v in story:
                msg += "%s\t-\t%s%s\n" % (v["date"], v["val"], v["currency"])

            update.message.reply_text(msg)
            update.message.reply_text("Это все, что получилось найти")

        else:
            update.message.reply_text(empty_result_message)
    else:
        print("bad url %s" % link)
        update.message.reply_text(invalid_query_text)


def error_callback(bot, update, error):
    print error



key = os.environ.get("KEY")

if (None == key):
    print "ERROR: KEY environment not set"
    os._exit(1)

updater = Updater(key)

f = Filters.text

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', hello))
updater.dispatcher.add_handler(MessageHandler(filters=f, callback=message_handler))
updater.dispatcher.add_handler(InlineQueryHandler(inline_hello))
updater.dispatcher.add_error_handler(error_callback)

updater.start_polling()
print "bot started"
updater.idle()
