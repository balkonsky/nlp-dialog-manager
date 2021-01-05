from core.models import Chat, BotState
from core.dialog_manager.fsm.scenario_logic import BotScenarioLogic
from loguru import logger


def on_new_chat_event(chat_id, language, order_id):
    bot_state = BotState.OPENING.value
    bot_chat = Chat.get_by(chat_id=chat_id)
    if bot_chat:
        bot_chat.delete()
    bot_chat = Chat(chat_id=str(chat_id), bot_state=str(bot_state), order_id=order_id, language=language)
    bot_chat.save()
    logger.debug(f'bot chat object from Redis {bot_chat}')
    scenario_logic = BotScenarioLogic(chat_id=bot_chat.chat_id, bot_chat=bot_chat)
    scenario_logic.transmit()


def on_new_message_event(chat_id, msg_text):
    bot_chat = Chat.get_by(chat_id=chat_id)
    logger.debug(f'get bot chat object from Redis {bot_chat}')
    bot_chat.client_message = msg_text
    bot_chat.save()
    logger.debug(f'bot chat object from Redis {bot_chat}')
    scenario_logic = BotScenarioLogic(bot_chat.chat_id, bot_chat)
    scenario_logic.transmit()


def on_new_file(files, chat_id):
    bot_chat = Chat.get_by(chat_id=chat_id)
    if len(files) > 1:
        bot_chat.bot_scenario_target_state_id = 'more_than_one_file'
        scenario_logic = BotScenarioLogic(bot_chat.chat_id, bot_chat)
        bot_chat.save()
        scenario_logic.transmit()
    elif len(files) > 0:
        bot_chat.client_file_link = files[0].url
        bot_chat.client_file_media_type = files[0].media_type
        bot_chat.client_file_name = files[0].name
        bot_chat.client_file_size = str(files[0].size)
        scenario_logic = BotScenarioLogic(bot_chat.chat_id, bot_chat)
        bot_chat.save()
        logger.debug(f'bot chat object from Redis {bot_chat}')
        scenario_logic.transmit()


def on_keyboard_response(chat_id, keyboard_response_button_text, keyboard_response_button_id):
    bot_chat = Chat.get_by(chat_id=chat_id)
    bot_chat.keyboard_response_button_text = keyboard_response_button_text
    bot_chat.keyboard_response_button_id = keyboard_response_button_id
    bot_chat.save()
    logger.debug(f'bot chat object from Redis {bot_chat}')
    scenario_logic = BotScenarioLogic(bot_chat.chat_id, bot_chat)
    scenario_logic.transmit()
