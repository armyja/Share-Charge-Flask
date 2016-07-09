from flask import Flask
import views

app = Flask(__name__)
# Load default config and override config from an environment variable
app.config.update(dict(
    # DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    # USERNAME='admin',
    # PASSWORD='default'
))

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/hello/', view_func=views.hello)
app.add_url_rule('/hello/<name>', view_func=views.hello)
app.add_url_rule('/login/', view_func=views.login, methods=['GET', 'POST'])
app.add_url_rule('/user/', view_func=views.user, methods=['GET'])
app.add_url_rule('/logout/', view_func=views.logout)

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')
