from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import uuid
import os


class OctoberryApp(Flask):
    def get_send_file_max_age(self, filename):
        if filename.lower().endswith('.html'):
            return None
        return Flask.get_send_file_max_age(self, filename)

app = OctoberryApp(__name__, static_url_path='')
mail = Mail(app)


@app.route('/', defaults={'lang': None})
@app.route('/<lang>')
def index_en(lang):
    if lang not in ['ru', 'en']:
        lang = 'ru' if 'ru' in request.host else 'en'
    return app.send_static_file('index_%s.html' % lang)


@app.route('/submit', methods=['POST'])
def contact_submit():
    result = jsonify({'result': True})
    data_to_send = (request.form['name'], request.form['email'], request.form['message'])
    if not any(data_to_send):
        return result
    message = u'Name: %s\nEmail: %s\nMessage:\n %s \n' % data_to_send
    current_dir = os.path.dirname(os.path.realpath(__file__))
    with open(current_dir + '/mails/' + str(uuid.uuid4()), 'a') as the_file:
        the_file.write(message.encode('utf8'))

    msg = Message("Message from site",
                  sender="team@octoberry.ru",
                  recipients=["team@octoberry.ru"],
                  body=message)
    try:
        mail.send(msg)
    except:
        pass
    return result

if __name__ == '__main__':
    app.run()
