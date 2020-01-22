import psutil
from telegram.ext import CommandHandler

from .. import dispatcher
from ..analysis.process_log_entry import AnalyseLogs
from ..commons import check_domain, query_ip
from ..conf import settings
from .decorators import auth, make_handler

Path = settings.Path
floor = settings.floor
datetime = settings.datetime
proc_base = settings.PROC_DIR
ten_mins = settings.TEN_MINUTES
one_day = settings.ONE_DAY
seven_days = settings.SEVEN_DAYS
half_month = settings.HALF_MONTH
thirty_days = settings.THIRTY_DAYS


@dispatcher.add_handler
@make_handler(CommandHandler, "resource")
@auth
def resource(update, context):
    cpu_percent = psutil.cpu_percent()
    swap_memory = psutil.swap_memory()
    virtual_memory = psutil.virtual_memory()
    mem_total = virtual_memory.total / (4 ** 10)
    mem_used = mem_total - (virtual_memory.available / 4 ** 10)
    swap_total = swap_memory.total / (4 ** 10)
    swap_used = swap_memory.used / (4 ** 10)
    sent_text = "CPU: %0.3f%%\nMemory: %0.3fMB / %0.3fMB\nSwap: %0.3fMB / %0.3fMB" % (
        cpu_percent,
        mem_used,
        mem_total,
        swap_used,
        swap_total,
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "uptime")
@auth
def uptime(update, context):
    try:
        with open(proc_base.joinpath('uptime').as_posix(), 'r') as fp:
            uptime = fp.read()
        uptime = floor(float(uptime.split(' ')[0]))
        now = datetime.now().strftime("%H:%M:%S")
        day = uptime / (24 * 3600)
        hours = int(uptime / 3600) % 24
        minutes = int(uptime / 60) % 60
        seconds = int(uptime % 60)
        sent_text = "%s, up %d %s %d:%d:%d" % (now, day, 'days' if day > 1 else 'day', hours, minutes, seconds)
    except FileNotFoundError:
        sent_text = 'None'
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "load")
@auth
def load(update, context):
    loadavg = 'None'
    with open(proc_base.joinpath("loadavg").as_posix(), 'r') as fp:
        loadavg = fp.read().strip('\n')
    context.bot.send_message(chat_id=update.effective_chat.id, text=loadavg)


@dispatcher.add_handler
@make_handler(CommandHandler, ["ping", "PING"])
@auth
def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="PONG")


@dispatcher.add_handler
@make_handler(CommandHandler, ['ip', 'IP'])
@auth
def ip(update, context):
    ip_data = query_ip(context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=ip_data)


@dispatcher.add_handler
@make_handler(CommandHandler, "start")
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


@dispatcher.add_handler
@make_handler(CommandHandler, "last10mins")
@auth
def last_10_mins(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no the domain's log to be analysed."
    if is_exists:
        sent_text = AnalyseLogs().start_analyse(domain=domain, datetime_range=ten_mins)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "last24hours")
@auth
def last_24_hours(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no the domain's log to be analysed."
    if is_exists:
        sent_text = AnalyseLogs().start_analyse(domain=domain, datetime_range=one_day)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "today")
@auth
def today(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no the domain's log to be analysed."
    if is_exists:
        start_datetime = end_datetime = datetime.now()
        this_year = end_datetime.year
        this_month = end_datetime.month
        this_day = end_datetime.day
        beg_datetime = datetime(year=this_year, month=this_month, day=this_day, hour=0, minute=0, second=0).timestamp()
        end_datetime = end_datetime.timestamp()
        sent_text = AnalyseLogs().start_analyse(
            domain=domain,
            start_datetime=start_datetime,
            datetime_range=end_datetime - beg_datetime
        )
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "last7days")
@auth
def last_7_days(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no domain to be analysed."
    if is_exists:
        sent_text = AnalyseLogs().start_analyse(domain=domain, datetime_range=seven_days)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "last14days")
@auth
def last_14_days(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no the domain's log to be analysed."
    if is_exists:
        sent_text = AnalyseLogs().start_analyse(domain=domain, datetime_range=half_month)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)


@dispatcher.add_handler
@make_handler(CommandHandler, "last30days")
@auth
def last_30_days(update, context):
    (domain, is_exists) = check_domain(context)
    sent_text = "There is no the domain's log to be analysed."
    if is_exists:
        sent_text = AnalyseLogs().start_analyse(domain=domain, datetime_range=thirty_days)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sent_text)
