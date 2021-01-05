"""
Models
======

"""

import rom
import enum

__all__ = ['MessageResponse', 'Message', 'FileMessage', 'FileData', 'Keyboard', 'Button',
           'Chat', 'BotState', 'ScenarioActionType', 'ScenarioLogic', 'ScenarioState', 'ScenarioStep',
           'ScenarioActionParameter', 'ScenarioConditionCheck', 'ScenarioButton', 'ScenarioAction']


class MessageResponse(object):
    def __init__(self, has_answer, messages):
        self.has_answer = has_answer
        self.messages = messages


class Message(object):
    def __init__(self, kind, text):
        self.kind = kind
        self.text = text


class FileMessage(object):
    def __init__(self, kind, data):
        self.kind = kind
        self.data = data


class FileData(object):
    def __init__(self, url, name, media_type):
        self.url = url
        self.name = name
        self.media_type = media_type


class Keyboard(object):
    def __init__(self, kind, buttons):
        self.kind = kind
        self.buttons = buttons


class Button(object):
    def __init__(self, id, text):
        self.id = id
        self.text = text


class Chat(rom.Model):
    chat_id = rom.Text(required=True, unique=True)
    bot_state = rom.Text()
    bot_scenario_state_id = rom.Text()
    bot_scenario_target_state_id = rom.Text()
    client_file_link = rom.Text()
    client_file_media_type = rom.Text()
    client_file_name = rom.Text()
    client_file_size = rom.Text()
    client_message = rom.Text()
    language = rom.Text()
    keyboard_response_button_id = rom.Text()
    keyboard_response_button_text = rom.Text()

    def __str__(self):
        return '({}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.chat_id, self.bot_state,
                                                                 self.bot_scenario_state_id,
                                                                 self.bot_scenario_target_state_id,
                                                                 self.client_file_link,
                                                                 self.client_file_media_type,
                                                                 self.client_file_name,
                                                                 self.client_file_size, self.client_message,
                                                                 self.language)


class BotState(enum.Enum):
    OPENING = 'opening'
    IDLE = 'idle'
    PROCESSING = 'processing'
    WAITING_FOR_RESPONSE = 'waiting_for_response'
    WAITING_FILE = 'waiting_file'
    REDIRECT_TO_QUEUE = 'redirect_to_queue'
    WAITING_RESPONSE_FROM_SERVICE = 'waiting_response_from_service'
    CLOSING = 'closing'
    CLOSE = 'close'
    # NEW_CHAT = 'new_chat'
    # SEND_MESSAGE = 'send_message'
    # WAIT_RESPONSE = 'wait_response'
    # RECEIVE_MESSAGE_RESPONSE = 'receive_message_response'
    # SEND_BUTTONS = 'send_buttons'
    # RECEIVE_BUTTON_RESPONSE = 'receive_button_response'
    # SEND_FILE = 'send_file'
    # RECEIVE_FILE = 'receive_file'
    # REDIRECT_TO_QUEUE = 'redirect_to_queue'
    # CLOSE_CHAT = 'close_chat'
    # SEND_REQUEST_TO_ANOTHER_SERVICE = 'send_request_to_another_service'
    # RECEIVE_RESPONSE_FROM_ANOTHER_SERVICE = 'receive_response_from_another_service'


class ScenarioActionType(enum.Enum):
    SEND_MESSAGE = 'send_message'
    SEND_FILE = 'send_file'
    SEND_BUTTONS = 'send_buttons'
    REDIRECT_TO_QUEUE = 'redirect_to_queue'
    CLOSE_CHAT = 'close_chat'
    SEND_REQUEST_TO_ANOTHER_SERVICE = 'send_request_to_another_service'
    CONDITION_CHECK = 'condition_check'
    WAITING_FOR_RESPONSE = 'waiting_for_response'
    WAITING_FILE = 'waiting_file'
    BUTTON_CHECK = 'button_check'
    SEND_FILE_TO_CLIENT = 'send_file_to_client'


class ScenarioLogic(object):
    def __init__(self, states, errors, general_properties):
        self.states = states
        self.errors = errors
        self.general_properties = general_properties


class ScenarioState(object):
    def __init__(self, state_id, is_init_state, title, actions, steps, is_final_state):
        self.state_id = state_id
        self.is_init_state = is_init_state
        self.is_final_state = is_final_state
        self.title = title
        self.actions = actions
        self.steps = steps


class ScenarioAction(object):
    def __init__(self, type, parameters):
        self.type = type
        self.parameters = parameters


class ScenarioStep(object):
    def __init__(self, step_id, state_id):
        self.step_id = step_id
        self.state_id = state_id


class ScenarioActionParameter(object):
    def __init__(self, ru_message_text=None, en_message_text=None, uz_message_text=None, file=None,
                 another_service_url=None, condition_check_param=None,
                 queue_name=None, buttons=None):
        self.ru_message_text = ru_message_text
        self.en_message_text = en_message_text
        self.uz_message_text = uz_message_text
        self.file = file
        self.another_service_url = another_service_url
        self.condition_check_param = condition_check_param
        self.queue_name = queue_name
        self.buttons = buttons


class ScenarioConditionCheck(object):
    def __init__(self, condition_id, success_check_step_id, fail_check_step_id):
        self.condition_id = condition_id
        self.success_check_step_id = success_check_step_id
        self.fail_check_step_id = fail_check_step_id


class ScenarioButton(object):
    def __init__(self, id, ru_message_text, en_message_text, uz_message_text, state_id):
        self.id = id
        self.ru_message_text = ru_message_text,
        self.en_message_text = en_message_text,
        self.uz_message_text = uz_message_text,
        self.state_id = state_id
