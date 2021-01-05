from fastapi import FastAPI, BackgroundTasks, Request
from base_models import ChatEventBody, ChatEventEnum, MessageKindEnum
from core.controllers.chat_controller import on_new_chat_event, on_new_message_event, on_new_file, \
    on_keyboard_response
from starlette import status
from starlette.responses import Response
from loguru import logger

app = FastAPI()


@app.post("/chatbot/v1/event/transmit")
async def chat_bot_action_transmit(chat_event: ChatEventBody, background_tasks: BackgroundTasks, request: Request):
    if chat_event.event == ChatEventEnum.new_chat:
        logger.debug(f'process new chat event with body: {chat_event}')
        background_tasks.add_task(on_new_chat_event, chat_event.chat.id, chat_event.chat.language,
                                  chat_event.visitor.field_value.orderId)
    elif chat_event.event == ChatEventEnum.new_message:
        logger.debug(f'process new message event with body: {chat_event}')
        if chat_event.message.kind == MessageKindEnum.file_visitor:
            logger.debug('run on_new_file handler')
            background_tasks.add_task(on_new_file, chat_event.message.data, chat_event.chat_id)
        elif chat_event.message.kind == MessageKindEnum.keyboard_response:
            logger.debug('run on_keyboard_response handler')
            background_tasks.add_task(on_keyboard_response, chat_event.chat_id, chat_event.message.data.button.text,
                                      chat_event.message.data.button.id)
        else:
            logger.debug('run on_new_message_event handler')
            background_tasks.add_task(on_new_message_event, chat_event.chat_id, chat_event.message.text)
    else:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    return {'result': 'ok'}
