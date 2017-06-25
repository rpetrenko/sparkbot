#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
    A simple bot script, built on Flask.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
# import json
# import requests
from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI, Webhook
from message_processor import MessageProcessor

# Initialize the environment
flask_app = Flask(__name__)
spark_api = CiscoSparkAPI()
message_processor = MessageProcessor()

urls = ('/sparkwebhook', 'webhook')


# Core bot functionality
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
                    <p>
                    <strong>Your Flask web server is up and running!</strong>
                    </p>
                    <p>
                    Here is a nice Cat Fact for you:
                    </p>
                    <blockquote> {} </blockquote>
                    </body>
                    </html>
                """.format("test is good"))
    elif request.method == 'POST':
        """Respond to inbound webhook JSON HTTP POST from Cisco Spark."""

        json_data = request.json                                               # Get the POST data sent from Cisco Spark
        # print("\n")
        # print("WEBHOOK POST RECEIVED:")
        # print(json_data)
        # print("\n")

        webhook_obj = Webhook(json_data)
        room_id = webhook_obj.data.roomId
        room = spark_api.rooms.get(room_id)
        data_id = webhook_obj.data.id
        try:
            message = spark_api.messages.get(data_id)
        except Exception:
            return 'OK'
        person_id = message.personId
        person = spark_api.people.get(person_id)
        message_text = message.text

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

            create_msg = "Got {}".format(message_text)
            print("SEND MESSAGE [{}]".format(create_msg))
            spark_api.messages.create(roomId=room_id, text=create_msg)
            response = message_processor.process(message_text)
            if response:
                spark_api.messages.create(roomId=room_id, text=response)
            return 'OK'


if __name__ == '__main__':
    # Start the Flask web server
    flask_app.run(host='0.0.0.0', port=5000)
