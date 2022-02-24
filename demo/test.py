# DialogHandler.py
# Handles the dialog between user and chat bot

# import dialogflow library
from google.cloud import dialogflow
from .credentials import PROJECT_ID, LANGUAGE_CODE
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service-account-file.json"


# Takes in user text and sends to DialogFlow for NLU
# Dialogflow reply with a text response (optional) with the intent (most useful) and other informations in JSON
def detect_intent_texts(session_id, text):
    '''
        Session_id: used to identify the session between user and dialogflow.
        A session is stored for 20 minutes in dialogflow. session_id can be a random number or string of
        user id as long as it does not exceed 36 bytes.

        texts: The list of texts from user. Dialogflow can receive multiple texts at once and return the
        intent for each texts.
    '''
    #   Set up a session with between end-user and dialogflow.
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(PROJECT_ID, session_id)
    #	print("Session path: {}\n".format(session))
    print(text, session)
    text_input = dialogflow.TextInput(text=text, language_code=LANGUAGE_CODE)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={
        "session": session,
        "query_input": query_input
    })

    #   print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

    return response


class DialogHandler(object):
    """
    Dialog handlers wraps the Dialogflow agent
    and provide handlers for intents
    """
    def __init__(self) -> None:
        super().__init__()
        self._session_client = dialogflow.SessionsClient()
        self._handlers = {}

    def detect(self, session_id, text, extras={}):
        session = self._session_client.session_path(PROJECT_ID, session_id)
        text_input = dialogflow.TextInput(text=text,
                                          language_code=LANGUAGE_CODE)
        query_input = dialogflow.QueryInput(text=text_input)
        response = self._session_client.detect_intent(
            request={
                "session": session,
                "query_input": query_input
            })
        intent = response.query_result.intent.display_name
        params = response.query_result.parameters if response.query_result.parameters else {}
        kwargs = {**params, **extras}
        print("kwargs", kwargs)
        if intent in self._handlers.keys():
            resp = self._handlers[intent](**kwargs)
        else:
            resp = {
                "type": 'plain',
                "message": "Sorry I cannot handle that intent"
            }

        return resp

    def register_handler(self, intent, handler):
        """
        handlers should be a function that takes in a dict
        of arguments and returns a dict of response
        The response dict is specified in the Documentation

        The handlers should also do error handling
        by calling abort defined in flask_restx
        """
        self._handlers[intent] = handler


dialog_handler = DialogHandler()