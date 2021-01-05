import json
import os

from loguru import logger
from core.models import (
    ScenarioLogic,
    ScenarioAction,
    ScenarioState,
    ScenarioStep,
    ScenarioActionType,
    ScenarioActionParameter,
    BotState,
    ScenarioConditionCheck,
    ScenarioButton,
    Button,
    Keyboard,
    Message,
    FileData,
    FileMessage
)
from core.controllers.actions_controller import send_message, redirect_chat, close_chat, get_file


class JsonScenario:
    obj = None
    data = None

    def __init__(self):
        raise Exception('call instance()')

    @classmethod
    def json_scenario(cls):
        if cls.obj is None:
            src = 'core/configs/scenario.json'
            if os.path.isfile(src):
                logger.debug(
                    'json_scenario_logic is None, set json from file...'
                )
                with open(src, encoding='utf-8') as json_file:
                    cls.data = json.load(json_file)
                    states = []
                    for state in cls.data.get('states'):
                        actions = []
                        for action in state.get('actions'):
                            action_type = ScenarioActionType(action.get('type')).name
                            parameters = action.get('parameters')
                            if action.get('type') == ScenarioActionType.CLOSE_CHAT.value:
                                actions.append(ScenarioAction(action_type, ScenarioActionParameter()))
                            if action.get('type') == ScenarioActionType.SEND_MESSAGE.value:
                                if parameters.get('ru_message_text'):
                                    param = ScenarioActionParameter(ru_message_text=parameters.get('ru_message_text'))
                                    actions.append(ScenarioAction(action_type, param))
                                if parameters.get('en_message_text'):
                                    param = ScenarioActionParameter(
                                        en_message_text=parameters.get('en_message_text'))
                                    actions.append(ScenarioAction(action_type, param))
                                if parameters.get('uz_message_text'):
                                    param = ScenarioActionParameter(
                                        uz_message_text=parameters.get('uz_message_text'))
                                    actions.append(ScenarioAction(action_type, param))
                            elif action.get('type') == ScenarioActionType.SEND_FILE.value:
                                pass
                            elif action.get('type') == ScenarioActionType.SEND_BUTTONS.value:
                                if parameters.get('buttons'):
                                    buttons = parameters.get('buttons')
                                    btns = []
                                    for button in buttons:
                                        btns.append(ScenarioButton(button.get('id'), button.get('ru_message_text'),
                                                                   button.get('en_message_text'),
                                                                   button.get('uz_message_text'),
                                                                   button.get('state_id')))
                                    actions.append(ScenarioAction(action_type, ScenarioActionParameter(buttons=btns)))
                            elif action.get('type') == ScenarioActionType.REDIRECT_TO_QUEUE.value:
                                if parameters.get('queue_name'):
                                    param = ScenarioActionParameter(queue_name=parameters.get('queue_name'))
                                    actions.append(ScenarioAction(action_type, param))
                            elif action.get('type') == ScenarioActionType.SEND_REQUEST_TO_ANOTHER_SERVICE.value:
                                pass
                            elif action.get('type') == ScenarioActionType.CONDITION_CHECK.value:
                                if parameters.get('condition_check_param'):
                                    condition_id = parameters.get('condition_check_param').get('condition_id')
                                    success_check_step_id = parameters.get('condition_check_param').get(
                                        'success_check_step_id')
                                    fail_check_step_id = parameters.get('condition_check_param').get(
                                        'fail_check_step_id')
                                    param = ScenarioActionParameter(
                                        condition_check_param=ScenarioConditionCheck(condition_id,
                                                                                     success_check_step_id,
                                                                                     fail_check_step_id))
                                    actions.append(ScenarioAction(action_type, param))
                            elif action.get('type') == ScenarioActionType.WAITING_FOR_RESPONSE.value:
                                pass

                            elif action.get('type') == ScenarioActionType.WAITING_FILE.value:
                                pass

                            elif action.get('type') == ScenarioActionType.SEND_FILE_TO_CLIENT.value:
                                url = parameters.get('url')
                                name = parameters.get('name')
                                media_type = parameters.get('media_type')
                                param = ScenarioActionParameter(file=FileData(url, name, media_type))
                                actions.append(ScenarioAction(action_type, param))

                        steps = []
                        if state.get('steps'):
                            for step in state.get('steps'):
                                steps.append(ScenarioStep(step.get('step_id'), step.get('state_id')))
                        if 'is_init_state' in state:
                            states.append(
                                ScenarioState(state.get('state_id'), state.get('is_init_state'), state.get('title'),
                                              actions, steps, False))
                        elif 'is_final_state' in state:
                            states.append(
                                ScenarioState(state.get('state_id'), False, state.get('title'),
                                              actions, steps, state.get('is_final_state')))
                        else:
                            states.append(
                                ScenarioState(state.get('state_id'), False, state.get('title'),
                                              actions, steps, False))
                    cls.obj = ScenarioLogic(states, cls.data.get('errors'), cls.data.get('general_properties'))
        logger.info(
            'set json_scenario_logic {}'.format(cls.data)
        )
        return cls


class BotScenarioLogic:

    def __init__(self, chat_id, bot_chat, json_scenario=JsonScenario.json_scenario().obj):
        self.chat_id = chat_id
        self.bot_chat = bot_chat
        self.json_scenario = json_scenario

    def transmit(self):
        self.bot_chat.bot_state = str(BotState.PROCESSING.value)
        self.bot_chat.save()
        if (self.bot_chat.bot_scenario_state_id is not None) & (
                self.bot_chat.bot_scenario_target_state_id is not None):
            if self.bot_chat.bot_scenario_state_id == self.bot_chat.bot_scenario_target_state_id:
                logger.info(
                    'we are in the current state and therefore must go to the next state {}'.format(
                        self.bot_chat.bot_scenario_state_id))
                current_state = self._get_state_by_id(self.bot_chat.bot_scenario_state_id)
                steps = current_state.steps
                self._steps_handler(steps)
            else:
                logger.debug(
                    'found a target state to move to {}'.format(self.bot_chat.bot_scenario_target_state_id))
                self.bot_chat.bot_scenario_state_id = self.bot_chat.bot_scenario_target_state_id
                self.bot_chat.save()
                target_state = self._get_state_by_id(self.bot_chat.bot_scenario_target_state_id)
                actions = target_state.actions
                self._actions_handler(actions)
        else:
            logger.debug(
                'found a first node')
            state = self._get_first_state()
            self.bot_chat.bot_scenario_state_id = state.state_id
            self.bot_chat.bot_scenario_target_state_id = state.state_id
            self.bot_chat.save()
            actions = state.actions
            self._actions_handler(actions)

    def _get_first_state(self):
        for state in self.json_scenario.states:
            if state.is_init_state:
                return state

    def _get_final_state(self):
        for state in self.json_scenario.states:
            if state.is_final_state:
                return state

    def _get_state_by_id(self, state_id):
        for state in self.json_scenario.states:
            if state.state_id == state_id:
                return state

    def _get_state_by_button_id(self, button_id):
        for state in self.json_scenario.states:
            for action in state.actions:
                if action.type == ScenarioActionType.SEND_BUTTONS.name:
                    for button in action.parameters.buttons:
                        if button.id == button_id:
                            return self._get_state_by_id(button_id.step_id)
        return None

    def _actions_handler(self, actions):
        logger.debug('receive actions to handle {}'.format(actions))
        for action in actions:
            logger.debug('actions handle with type {}'.format(action.type))
            if action.type == ScenarioActionType.SEND_MESSAGE.name:
                if self.bot_chat.language == 'ru':
                    if action.parameters.ru_message_text:
                        ru_message = Message('', action.parameters.ru_message_text)
                        send_message(self.chat_id, ru_message)
                elif self.bot_chat.language == 'en':
                    if action.parameters.en_message_text:
                        en_message = Message('', action.parameters.en_message_text)
                        send_message(self.chat_id, en_message)
                elif self.bot_chat.language == 'uz':
                    if action.parameters.uz_message_text:
                        uz_message = Message('', action.parameters.uz_message_text)
                        send_message(self.chat_id, uz_message)
            elif action.type == ScenarioActionType.SEND_FILE:
                pass
            elif action.type == ScenarioActionType.SEND_BUTTONS.name:
                btns = []
                for button in action.parameters.buttons:
                    if self.bot_chat.language == 'ru':
                        if button.ru_message_text:
                            btns.append([Button(button.id, button.ru_message_text[0]).__dict__])
                    elif self.bot_chat.language == 'en':
                        if button.en_message_text:
                            btns.append([Button(button.id, button.en_message_text[0]).__dict__])
                    elif self.bot_chat.language == 'uz':
                        if button.uz_message_text:
                            btns.append([Button(button.id, button.uz_message_text[0]).__dict__])
                if len(btns) > 0:
                    keyboard = Keyboard('keyboard', btns)
                    send_message(self.chat_id, keyboard)
            elif action.type == ScenarioActionType.REDIRECT_TO_QUEUE.name:
                redirect_chat(self.bot_chat.language, action.parameters.queue_name, self.chat_id)
            elif action.type == ScenarioActionType.CLOSE_CHAT.name:
                close_chat(self.chat_id)
            elif action.type == ScenarioActionType.SEND_REQUEST_TO_ANOTHER_SERVICE.name:
                pass
            elif action.type == ScenarioActionType.CONDITION_CHECK.name:
                condition_id = action.parameters.condition_check_param.condition_id
                success_check_step_id = action.parameters.condition_check_param.success_check_step_id
                fail_check_step_id = action.parameters.condition_check_param.fail_check_step_id
                condition_check = self.get_condition_by_id(condition_id)
                steps = self._get_state_by_id(self.bot_chat.bot_scenario_state_id).steps
                if condition_check():
                    logger.debug('success check step with step_id {}'.format(success_check_step_id))
                    self._steps_handler(steps=steps, step_id=success_check_step_id)
                else:
                    logger.debug('fail check step with step_id {}'.format(fail_check_step_id))
                    self._steps_handler(steps=steps, step_id=fail_check_step_id)
            elif action.type == ScenarioActionType.BUTTON_CHECK.name:
                if self.bot_chat.keyboard_response_button_id:
                    target_state = self._get_state_by_button_id(self.bot_chat.keyboard_response_button_id)
                    if target_state:
                        target_state_id = target_state.state_id
                        self.bot_chat.bot_scenario_target_state_id = target_state_id
                        self.bot_chat.save()
                        self.transmit()
            elif action.type == ScenarioActionType.SEND_FILE_TO_CLIENT.name:
                file = FileMessage('file_operator', action.parameters.file.__dict__)
                send_message(self.chat_id, file)

    def _steps_handler(self, steps, **kwargs):
        if 'step_id' in kwargs:
            if len(steps) > 1:
                target_state_id = None
                for step in steps:
                    if step.step_id == kwargs.get('step_id'):
                        target_state_id = step.state_id
                        break
                if target_state_id:
                    logger.debug(
                        'update bot chat object and transmit new state with id {}'.format(target_state_id))
                    self.bot_chat.bot_scenario_target_state_id = target_state_id
                    self.bot_chat.save()
                    self.transmit()
        else:
            if len(steps) == 1:
                target_state_id = steps[0].state_id
                logger.debug(
                    'update bot chat object and transmit new state with id {}'.format(target_state_id))
                self.bot_chat.bot_scenario_target_state_id = target_state_id
                self.bot_chat.save()
                self.transmit()

    def is_file_correct(self):
        if self.bot_chat.client_file_link:
            if self.bot_chat.client_file_media_type in ['image/png', 'image/jpeg', 'image/jpg']:
                return True
        return False

    def is_order_receive(self):
        if self.bot_chat.order_id:
            return True
        return False

    def is_receive_buttons(self):
        if (self.bot_chat.keyboard_response_button_id is not None) & (
                self.bot_chat.keyboard_response_button_text is not None):
            return True
        return False

    def get_condition_by_id(self, condition_id):

        if condition_id == '1003':
            return self.is_file_correct

        elif condition_id == '1004':
            return self.is_order_receive

        elif condition_id == '1008':
            return self.is_receive_buttons
