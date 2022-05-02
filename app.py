from website import create_app
from flask import render_template

app = create_app()

def page_not_found(e):
  return render_template('error_page.html'), 404

if __name__ == '__main__':
    # current IPV4
    app.register_error_handler(404, page_not_found)
    app.run('0.0.0.0', port=5000, debug=True, ssl_context='adhoc')