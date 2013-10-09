from flask import Flask, g, request, jsonify, render_template
from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config.from_object('city_autocomplete.config')

@app.route('/', methods=['GET'])
def home():
    return render_template('index.jinja2')

@app.route('/search/', methods=['GET'])
def search():
    search_term = request.args.get('search_term')
    if search_term:
        try:
            search_query = {"name":
                                {
                                    "text": search_term,
                                    "completion": {
                                        "field": "suggest"
                                    }
                                }
                            }
            results = g.es.suggest(body=search_query,
                                   index=app.config['INDEX_NAME'])
            options = results["name"][0]["options"]
        except Exception as e:
            print e
            return jsonify({'status': 'ERROR'})
        result_data = {'status': 'SUCCESS',
                       'results': options}
        return jsonify(result_data)
    else:
        return jsonify({})


@app.before_request
def before_request():
    try:
        g.es = Elasticsearch()
    except Exception as e:
        print e
        return jsonify({'status': 'ERROR'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
