from flask import Flask, g, session, request, redirect, flash, abort, session, url_for
from flask_mail import Mail
from shotglass2 import shotglass
from shotglass2.takeabeltof.database import Database
from shotglass2.takeabeltof.jinja_filters import register_jinja_filters
from shotglass2.users.admin import Admin

# Create app
# setting static_folder to None allows me to handle loading myself
app = Flask(__name__, instance_relative_config=True,
        static_folder=None)
app.config.from_pyfile('site_settings.py', silent=True)

@app.before_first_request
def start_logging():
    shotglass.start_logging(app)

@app.context_processor
def inject_site_config():
    # Add 'site_config' dict to template context
    return {'site_config':shotglass.get_site_config()}

# work around some web servers that mess up root path
from werkzeug.contrib.fixers import CGIRootFix
if app.config['CGI_ROOT_FIX_APPLY'] == True:
    fixPath = app.config.get("CGI_ROOT_FIX_PATH","/")
    app.wsgi_app = CGIRootFix(app.wsgi_app, app_root=fixPath)

register_jinja_filters(app)


mail = Mail(app)

def init_db(db=None):
    # to support old code
    initalize_all_tables(db)

def initalize_all_tables(db=None):
    """Place code here as needed to initialze all the tables for this site"""
    if not db:
        db = get_db()
        
    shotglass.initalize_user_tables(db)
    
    ### setup any other tables you need here....
    
    
def get_db(filespec=None):
    """Return a connection to the database.
    If the db path does not exist, create it and initialize the db"""
    
    if not filespec:
        filespec = shotglass.get_site_config()['DATABASE_PATH']
        
    # This is probobly a good place to change the
    # filespec if you want to use a different database
    # for the current request.
    
        
    # test the path, if not found, create it
    initialize = shotglass.make_db_path(filespec)
        
    g.db = Database(filespec).connect()
    if initialize:
        initalize_all_tables(g.db)
            
    return g.db
    
    
@app.context_processor
def inject_site_config():
    # Add 'site_config' dict to template context
    return {'site_config':shotglass.get_site_config()}


@app.before_request
def _before():
    # Force all connections to be secure
    if app.config['REQUIRE_SSL'] and not request.is_secure :
        return redirect(request.url.replace("http://", "https://"))

    #ensure that nothing is served from the instance directory
    if 'instance' in request.url:
        return abort(404)
        
    #import pdb;pdb.set_trace()

    session.permanent = True
    
    shotglass.get_site_config(app)
    shotglass.set_template_dirs(app)
    
    get_db()
    
    # Is the user signed in?
    g.user = None
    if 'user' in session:
        g.user = session['user']
        
        
    #g.menu_items = shotglass.get_menu_items()
    g.menu_items = [
        {'title':'Home','url':'/'},
        # {'title':'RSVP','url':url_for('www.rsvp')},
        # {'title':'Where to Stay','url':url_for('www.render_for', filename='where_to_stay')},
        # {'title':'Things to Do','url':url_for('www.render_for', filename='things_to_do')},
        # {'title':'Shopping','url':url_for('www.render_for', filename='shopping')},
        # {'title':'The Menu','url':url_for('www.render_for', filename='menu')},
        # {'title':'Churches','url':url_for('www.render_for',filename='churches')},
        # {'title':'Questions','url':url_for('www.contact')},
        ]
        
    g.admin = Admin(g.db) # This is where user access rules are stored
    shotglass.user_setup() # g.admin now holds access rules Users, Prefs and Roles

@app.teardown_request
def _teardown(exception):
    if 'db' in g:
        g.db.close()


@app.errorhandler(404)
def page_not_found(error):
    return shotglass.page_not_found(error)

@app.errorhandler(500)
def server_error(error):
    return shotglass.server_error(error)

#Register the static route
app.add_url_rule('/static/<path:filename>','static',shotglass.static)

# To use a different subdomain as asset server, use this instead
# Direct to a specific server for static content
#app.add_url_rule('/static/<path:filename>','static',shotglass.static,subdomain="somesubdomain")


## Setup the routes for users
shotglass.register_users(app)

# setup www.routes...
# shotglass.register_www(app)
from www.views import home
app.register_blueprint(home.mod)

if __name__ == '__main__':
    
    with app.app_context():
        # create the default database if needed
        initalize_all_tables()
        
    #app.run(host='localhost', port=8000)
    app.run()
    
    