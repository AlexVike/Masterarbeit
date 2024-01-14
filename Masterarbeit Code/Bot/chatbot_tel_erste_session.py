# Grundgerüst von https://docs.aiogram.dev/en/latest/ Tutorial für den Chatbot
# Docs mit Github Copilot geschrieben

import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters import Command
from aiogram.filters import Filter
from aiogram.types import Message, PollAnswer
from aiogram.utils.markdown import hbold
from datetime import datetime, timedelta


from gpt_lerncoach_neutral import OpenAiInterface
from messages import UNIFIED_INTRO_MESSAGE, start, end_chat


# Bot token can be obtained via https://t.me/BotFather

TOKEN = "6598818083:AAGP9RIBAq_5enef0sYMm-OqcSKbG_JvyWc" # Live
#TOKEN = "6843369687:AAFpvBX0lgFYSRfFa3c_9hzmAYinz8J3x_Y" # Production
# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()

tmp: OpenAiInterface | None = None
lock = asyncio.Lock()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    
    global tmp
    if (msg := message.from_user) is not None:
        await message.answer(f"Hallo, {hbold(msg.full_name)}!")
        # chat_id_base62 = await tmp.encode_base62(message.chat.id)
        # print(f"Chat ID {message.chat.id} is encoded to {chat_id_base62}")
        # print(
        #     f"Chat ID {chat_id_base62} is decoded to {await tmp.decode_base62(chat_id_base62)}"
        # )
        await message.answer(start.format(message.chat.id), parse_mode=ParseMode.HTML)
        await message.answer("Mila leitet das Gespräch bis zu einem vordefinierten Endpunkt der Studie. Wenn du zufrieden mit dem Ergebnis bist, oder aus einem anderen Grund das Gespräch beenden möchtest, tippe /end.")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    This handler receives messages with `/help` command
    """
    await message.answer("Bitte schreibe eine Nachricht an @Masterarbeit_Vikete")
    await message.answer_contact("+491745476282", "Alexander")


@dp.message(Command("end"))
async def poll(message: types.Message):
    """
    Handles the 'end' command by checking the number of turns taken in the chat and providing appropriate responses.
    
    Args:
        message (types.Message): The message object containing the command.
    """
    number_turns = await tmp.count_interactions(chat_id=message.chat.id)
    print(number_turns)
    number_turns_left = 6 - number_turns
    if number_turns < 6:
        await message.answer(
            f"Du kannst den Chat noch nicht beenden. Bitte schreibe noch {number_turns_left} Nachrichten an den Chatbot. Falls ein Problem aufgetaucht ist, schreibe bitte eine Nachricht an @Masterarbeit_Vikete."
        )
        return
    await message.answer_poll(
        question="Bist du dir sicher, dass du den Chat vorläufig beenden möchtest?",
        options=[
            "Ja",
            "Nein",
            "Ich möchte den Chat beenden, aber bei der zweiten Session wieder teilnehmen.",
        ],
        is_anonymous=False,
    )
    
@dp.message(Command("posttest"))
async def posttest(message: Message) -> None:
    """
    This handler receives messages with `/posttest` command
    and sends a response with a link to the posttest form.

    Parameters:
    - message (Message): The message object received from the user.

    Returns:
    None
    """
    print(f"postest {message.chat.id}")
    await message.answer("Vielen Dank, dass du dir die Zeit nimmst den Posttest auszufüllen: <a href='https://docs.google.com/forms/d/e/1FAIpQLSfdakpHPgq1O-DbIAzPX02Aycrlkae4Rqm4Mw3UHODtTbEuEw/viewform?entry.592158190={}'>Posttest</a>".format(message.chat.id))


@dp.poll_answer()
async def poll_answer(poll_answer: types.PollAnswer):
    """
    Handles the user's poll answer and performs corresponding actions based on the selected option.

    Args:
        poll_answer (types.PollAnswer): The poll answer object containing the user's selection.

    Returns:
        None
    """
    answer_ids = poll_answer.option_ids  # list of answers
    if answer_ids[0] == 0:
        await poll_answer.bot.send_message(
            poll_answer.user.id, end_chat.format(poll_answer.user.id)
        )
        await tmp.insert_into_end_chat(chat_id=poll_answer.user.id)
    elif answer_ids[0] == 1:
        await poll_answer.bot.send_message(
            poll_answer.user.id,
            "Du kannst den Chat normal bei deiner letzten Nachricht fortsetzen.",
        )
    else:
        await poll_answer.bot.send_message(
            poll_answer.user.id, end_chat.format(poll_answer.user.id)
        )
        await tmp.insert_into_end_chat(chat_id=poll_answer.user.id)
        await tmp.insert_into_anmeldung(chat_id=poll_answer.user.id)
    print(answer_ids)


MAX_MESSAGE_LENGTH = 350


# The above code is a Python function that serves as a message handler for a chatbot. It receives a
# message from a user and performs various actions based on the content of the message.
@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

   
    """
    try:
        # Send a copy of the received message
        global tmp
        chat_id = message.chat.id
        get_info = await tmp.get_combined_info(chat_id)
        # Zewite Session. Nach der ersten Session, falls die Teilnehmer*innen sich für die zweite Session angemeldet haben und die erste Session abgeschlossen haben, werden sie in die zweite Session weitergeleitet. Jedoch  muss eine Woche vergangen sein.
        # Wenn get_info[3] nicht None ist und get_info[4] einen gültigen Wert hat
        if get_info[2] is not None and get_info[3] is not None:
            # Wandeln Sie den Unix-Zeitstempel in ein datetime-Objekt um
            timestamp_datetime = datetime.utcfromtimestamp(get_info[3])

            
            one_week_later = timestamp_datetime + timedelta(days=7)
            one_week_later = one_week_later.replace(hour=0, minute=1)

            # Aktuelles Datum und Uhrzeit
            current_datetime = datetime.utcnow()

            if current_datetime <= one_week_later:
            # Berechnen der verbleibenden Zeit
                remaining_time = one_week_later - current_datetime

                # Formatieren der verbleibenden Zeit in Tage, Stunden und Minuten
                days = remaining_time.days
                hours, remainder = divmod(remaining_time.seconds, 3600)
                minutes = remainder // 60

                # Aktualisieren der Nachricht mit der verbleibenden Zeit
                await message.answer(
                    f"Bitte warte noch {days} Tage, {hours} Stunden und {minutes} Minuten. "
                    "Melde dich, falls noch nicht geschehen, über den <a href='https://elearning.uni-regensburg.de/mod/choice/view.php?id=2503284'>Grips Link</a> für die zweite Session an."
                )
                return

            
            elif current_datetime >= one_week_later:
                gruppe = get_info[1]
                print(gruppe)
                phase_zweite_session = await tmp.get_last_phase_zweite_session(
                    chat_id=message.chat.id
                )
                if gruppe == "NC":
                    if len(message.text) > MAX_MESSAGE_LENGTH:
                        print(len(message.text))
                        await message.answer(
                            "Bitte schreibe eine kürzere Nachricht an den Chatbot"
                        )
                        return
                    if (msg_text := message.text) is not None:
                        print("phase_zweite_session, neutraler chatbot")
                        
                        if phase_zweite_session is None:
                            print("None, neutraler chatbot")
                            print(phase_zweite_session)
                            last_summary = await tmp.get_last_summary_by_id(chat_id)
                            bot_response = "Hallo, schön, dass du wieder da bist.\n" + "In der letzten Session haben wir folgendes diskutiert:\n" + last_summary + "\n" + "Konntest du schon seit unserer letzten Session Fortschritte erzielen?"
                            await message.answer(bot_response)
                            await tmp.update_database_zweite_session(chat_id=chat_id, message=msg_text, response=bot_response, phase=1, Gruppe="NC")
                        elif phase_zweite_session == 1:
                            print("1, neutraler chatbot")
                            print(phase_zweite_session)
    
                            msg = await tmp.get_response_neutral_zweite_session(chat_id=chat_id, message=msg_text)
                            await message.answer(msg)
                    else:
                        await message.answer("Es ist ein Fehler aufgetreten")
                        raise ValueError
                    return
                elif gruppe == "LC":
                    if len(message.text) > MAX_MESSAGE_LENGTH:
                        print(len(message.text))
                        await message.answer(
                            "Bitte schreibe eine kürzere Nachricht an den Chatbot"
                        )
                        return
                    if (msg_text := message.text) is not None:
                        if phase_zweite_session is None:
                            last_summary = await tmp.get_last_summary_by_id(chat_id)
                            bot_response = "Hallo, schön, dass du wieder da bist.\n" + "In der letzten Session haben wir folgendes diskutiert:\n" + last_summary + "\n" + "Konntest du schon seit unserer letzten Session Fortschritte erzielen? Bitte schreibe 'Ja' oder 'Nein'."
                            await message.answer(bot_response)
                            await tmp.update_database_zweite_session(chat_id=chat_id, message=msg_text, response=bot_response, phase=1)
                        elif phase_zweite_session == 1:
                            if msg_text == "Ja" or msg_text == "ja":
                                await tmp.insert_into_fortschritt(chat_id=chat_id, fortschritt= "Ja")
                                msg = await tmp.get_bot_response_phase2_zweite_session(
                                    chat_id=message.chat.id, message=msg_text
                                )
                                await message.answer(msg)
                            elif msg_text == "Nein" or msg_text == "nein":
                                await tmp.insert_into_fortschritt(chat_id=chat_id, fortschritt= "Nein")
                                msg = await tmp.get_bot_response_phase2_zweite_session(
                                    chat_id=message.chat.id, message=msg_text
                                )
                                await message.answer(msg)
                            else:
                                await message.answer("Bitte antworte mit Ja oder Nein")
                        elif phase_zweite_session == 2:
                            msg = await tmp.get_bot_response_phase2_zweite_session(
                                    chat_id=message.chat.id, message=msg_text
                                )
                            await message.answer(msg)
                        elif phase_zweite_session == 3:
                            msg = await tmp.get_bot_response_phase3_zweite_session(
                                    chat_id=message.chat.id, message=msg_text
                                )
                            await message.answer(msg)
                        elif phase_zweite_session == 4:
                            msg = await tmp.get_bot_response_phase4_zweite_session(
                                    chat_id=message.chat.id, message=msg_text
                                )
                            await message.answer(msg)
                        elif phase_zweite_session == 5:
                            await message.answer("Vielen Dank für deine Teilnahme!")
                            return                        
                    else:
                        await message.answer("Es ist ein Fehler aufgetreten")
                        raise ValueError
                    return
        print(get_info)
        # Der Chat wurde früher beendet, aber die Teilnehmer*innen haben sich nicht für die zweite Session angemeldet.
        if get_info[4]:
            await message.answer("Vielen Dank für deine Teilnahme!")
            return
        is_chat_id_in_db = get_info[0]
        print(is_chat_id_in_db)
        # Erste Session. LC und NC gleichzeitig, auf Basis der Aufteilung in der Datenbank, gerade oder ungerade Anzahl an Chat IDs
        if is_chat_id_in_db:
            print(f"Chat ID {chat_id} is in database")
            gruppe = get_info[1]
            print(gruppe)
            if gruppe == "NC":
                if len(message.text) > MAX_MESSAGE_LENGTH:
                    print(len(message.text))
                    await message.answer(
                        "Bitte schreibe eine kürzere Nachricht an den Chatbot"
                    )
                    return
                phase_n = await tmp.get_last_phase(chat_id=message.chat.id)
                if phase_n == 5:
                    if message.text == "Ja" or message.text == "ja":
                        await message.answer(
                                end_chat.format(message.chat.id)
                            )
                        await tmp.update_database_neutral(
                            chat_id=chat_id, message="", response="", phase=6
                        )
                        await tmp.insert_into_anmeldung(chat_id=chat_id)
                    elif message.text == "Nein" or message.text == "nein":
                        await message.answer(end_chat.format(message.chat.id))
                        await tmp.update_database_neutral(
                            chat_id=chat_id, message="", response="", phase=6
                        )
                elif phase_n == 6:
                    await message.answer("Vielen Dank für deine Teilnahme!")
                else:
                    mesg = await tmp.get_response_neutral(
                        chat_id=chat_id, message=message.text
                    )
                    await message.answer(mesg)
            elif gruppe == "LC":
                if len(message.text) > MAX_MESSAGE_LENGTH:
                    print(len(message.text))
                    await message.answer(
                        "Bitte schreibe eine kürzere Nachricht an den Chatbot"
                    )
                    return
                if (msg_text := message.text) is not None:
                    phase = await tmp.get_last_phase(chat_id=message.chat.id)
                    if phase is None:
                        msg = await tmp.get_bot_response_phase2(
                            chat_id=message.chat.id, message=msg_text
                        )
                        await message.answer(msg)
                    elif phase == 2:
                        msg = await tmp.get_bot_response_phase2(
                            chat_id=message.chat.id, message=msg_text
                        )
                        await message.answer(msg)
                    elif phase == 2.1:
                        msg = await tmp.get_bot_response_phase2_1(
                            chat_id=message.chat.id, message=msg_text
                        )
                        await message.answer(msg)
                    elif phase == 3:
                        msg = await tmp.phase_drei(
                            chat_id=message.chat.id, message=msg_text
                        )
                        await message.answer(msg)
                    elif phase == 4:
                        msg = await tmp.get_bot_response_phase4(
                            chat_id=message.chat.id, message=msg_text
                        )
                        await message.answer(msg)
                    elif phase == 5:
                        if msg_text == "Ja" or msg_text == "ja":
                            await message.answer(
                                end_chat.format(message.chat.id)
                            )
                            await tmp.update_database(
                                chat_id=chat_id, message="", response="", phase=6
                            )
                            await tmp.insert_into_anmeldung(chat_id=chat_id)
                        elif msg_text == "Nein" or msg_text == "nein":
                            await message.answer(end_chat.format(message.chat.id))
                            await tmp.update_database(
                                chat_id=chat_id, message="", response="", phase=6
                            )
                        else:
                            await message.answer("Bitte antworte mit Ja oder Nein")
                    elif phase == 6:
                        await message.answer("Vielen Dank für deine Teilnahme!")
                else:
                    await message.answer("Es ist ein Fehler aufgetreten")
                    raise ValueError
        # Bei der ersten Nachricht werden die Leute aufgeteilt in die 2 Gruppen. Die erste Nachricht wird nicht gespeichert. Die Leute müsssen Chatbot schreiben, um in die erste Session zu kommen.
        else:
            async with lock:
                if message.text == "Chatbot" or message.text == "chatbot":
                    unique_chat_ids_count = await tmp.get_unique_chat_ids_count()
                    print(unique_chat_ids_count)
                    if unique_chat_ids_count % 2 == 0:
                        if len(message.text) > MAX_MESSAGE_LENGTH:
                            print(len(message.text))
                            await message.answer(
                                "Bitte schreibe eine kürzere Nachricht an den Chatbot"
                            )
                            return
                        await tmp.update_database(
                            chat_id=chat_id, message="", response="", phase=2
                        )
                        await message.answer(UNIFIED_INTRO_MESSAGE)
                    else:
                        await tmp.update_database_neutral(
                            chat_id=chat_id, message="", response=""
                        )
                        await message.answer(UNIFIED_INTRO_MESSAGE)
                else:
                    await message.answer(
                        "Bitte fülle zuerst den Fragebogen aus. Danke! Der Link zum Fragebogen bekommst du wenn du /start schreibst."
                    )

        

    except TypeError:
        
        await message.answer("Bitte verschicke nur Textnachrichten an den Chatbot")


async def main() -> None:
    
    oai_interface = OpenAiInterface()
    global tmp
    tmp = oai_interface

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
