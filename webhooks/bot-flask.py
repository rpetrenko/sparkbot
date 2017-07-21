#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    A simple bot script, built on Flask.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
import os
from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI, Webhook
import requests
from requests import ConnectionError

flask_app = Flask(__name__)
spark_api = CiscoSparkAPI()

urls = ('/sparkwebhook', 'webhook')

# url for posting messages to message processing server
MP_POST_URL = os.environ.get('MP_POST_URL', 'http://localhost:9001/mp')


def send_message(room_id, msg):
    print("SEND MESSAGE [{}]".format(msg))
    spark_api.messages.create(roomId=room_id, text=msg)


@flask_app.route('/sparkwebhook', methods=['GET', 'POST'])
# Your Spark webhook should point to http://<serverip>:5000/sparkwebhook
def sparkwebhook():
    """Processes incoming requests to the '/sparkwebhook' URI."""
    if request.method == 'GET':
        return (""" <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title>Spark Bot served via Flask</title>
                        </head>
                        <body>
                            <p><strong>Your Flask web server is up and running!!!</strong></p>
                            <p>Status:</p>
                            <blockquote> {} </blockquote>
                        </body>
                    </html>
                """.format("test is good"))
    elif request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Cisco Spark."""

        json_data = request.json
        print("json_data", json_data)
        webhook_obj = Webhook(json_data)
        print("webhook_ojb", webhook_obj)
        room_id = webhook_obj.data.roomId
        print("room_id", room_id)
        room = spark_api.rooms.get(room_id)
        print("room", room)
        data_id = webhook_obj.data.id
        print("data_id", data_id)
        try:
            message = spark_api.messages.get(data_id)
            print("message", message)
        except Exception as e:
            print("exception", e)
            return 'OK'
        person_id = message.personId
        print("person_id", person_id)
        person = spark_api.people.get(person_id)
        print("person", person)
        message_text = message.text
        print("messsage_text", message_text)

        # This is a VERY IMPORTANT loop prevention control step.
        # If you respond to all messages...  You will respond to the messages
        # that the bot posts and thereby create a loop condition.
        me = spark_api.people.me()
        if message.personId == me.id:
            # Message was sent by me (bot); do not respond.
            return 'OK'
        else:
            print("NEW MESSAGE IN ROOM '{}'".format(room.title))
            print("FROM '{}'".format(person.displayName))
            print("MESSAGE '{}'\n".format(message_text))

            create_msg = "Processing {}".format(message_text)
            send_message(room_id, create_msg)

            print("posting msg", message_text)
            try:
                result = requests.post(MP_POST_URL, data=message_text)
                if result.ok:
                    result = result.text
                    if result:
                        send_message(room_id, str(result))
                    send_message(room_id, "Done")
            except ConnectionError as e:
                send_message(room_id, str(e))
            return 'OK'


if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5000)
