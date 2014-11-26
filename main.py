#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from testModel import *
import os
import webapp2
import jinja2


jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


#User Input Class
class user_input:
    def __init__(self, rev_type, text):
        self.rev_type = rev_type
        self.text = text

    def classify(self):
        review = self.text.split(" ")
        if self.rev_type == 'Book':
            books_model = read_file('books_model')
            return classifyInput(review, books_model)
        elif self.rev_type == 'DVD':
            dvd_model = read_file('dvd_model')
            return classifyInput(review, dvd_model)
        elif self.rev_type == 'Electronics':
            electronics_model = read_file('electronics_model')
            return classifyInput(review, electronics_model)
        elif self.rev_type == 'Kitchen':
            kitchen_model = read_file('kitchen_model')
            return classifyInput(review, kitchen_model)
        return [0.2, 0.2, 0.2, 0.2, 0.2]


    def get_Sentiment(self, res):
        pos = res[3] + res[4]
        neg  = res[0] + res[1]

        if pos > neg:
            return ['Positive Review', 'glyphicon glyphicon-thumbs-up']
        elif pos < neg:
            return ['Negative Review', 'glyphicon glyphicon-thumbs-down']
        else:
            return ['Ambiguous Review', 'glyphicon glyphicon-question-sign']

    def sentiment_prob(self, res):
        pos = res[3] + res[4]
        neg = res[0] + res[1]

        if pos > neg:
            return pos
        elif pos < neg:
            return neg
        else:
            return res[2]

    def predict_rating(self, res):
        return res.index(max(res)) + 1

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        contact = jinja_environment.get_template('contact.html')
        self.response.out.write(contact.render())

class FeaturesHandler(webapp2.RequestHandler):
    def get(self):
        contact = jinja_environment.get_template('features.html')
        self.response.out.write(contact.render())

class ModalHandler(webapp2.RequestHandler):
    def post(self):
        review = self.request.get('productReview')
        input_type = self.request.get('inputType')

        x = user_input(input_type, review)
        x_res = x.classify()
        x_rating = x.predict_rating(x_res)
        x_sentiment = x.get_Sentiment(x_res)
        x_confidence = int(round(x.sentiment_prob(x_res)*100))
        x_one = round(x_res[0], 3)
        x_two = round(x_res[1], 3)
        x_three = round(x_res[2], 3)
        x_four = round(x_res[3], 3)
        x_five = round(x_res[4], 3)

        modal_values = {
            'type': input_type,
            'one': x_one,
            'two': x_two,
            'three': x_three,
            'four': x_four,
            'five': x_five,
            'rating': x_rating,
            'sentiment_txt': x_sentiment[0],
            'sentiment_img': x_sentiment[1],
            'confidence': x_confidence
        }

        modal = jinja_environment.get_template('modal.html')
        self.response.out.write(modal.render(modal_values))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/modal', ModalHandler),
    ('/features', FeaturesHandler),
    ('/contact', ContactHandler)
], debug=True)
