from flask import Flask, request, jsonify
from flask_mail import Mail, Message


class OctoberryApp(Flask):
    def get_send_file_max_age(self, filename):
        if filename.lower().endswith('.html'):
            return None
        return Flask.get_send_file_max_age(self, filename)

app = OctoberryApp(__name__, static_url_path='')
mail = Mail(app)


@app.route('/ru')
def index_ru():
    return app.send_static_file('index_ru.html')


@app.route('/')
@app.route('/en')
def index_en():
    return app.send_static_file('index_en.html')


@app.route('/submit', methods=['POST'])
def contact_submit():
    message = 'Name: %s\nEmail: %s\nMessage:\n %s \n' % (request.form['name'], request.form['email'], request.form['message'])

    msg = Message("Message from site",
                  sender="team@octoberry.ru",
                  recipients=["team@octoberry.ru"],
                  body=message)
    mail.send(msg)
    return jsonify({'result': True})

if __name__ == '__main__':
    app.debug = True
    app.run()
