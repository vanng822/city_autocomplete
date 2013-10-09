from flask import Flask, g, request, jsonify
from pyelasticsearch import ElasticSearch


app = Flask(__name__)
app.config.from_object('city_autocomplete.config')


@app.route('/', methods=['GET'])
def get_suggestions():
    search_term = request.args.get('search_term')
    if search_term:
        try:
            results = g.es.search('{field}:{term}'.format(field=app.config['SEARCH_FIELD'],
                                                          term=search_term),
                                  index=app.config['INDEX_NAME'])
        except:
            return jsonify({'status': 'ERROR'})
        result_data = {'status': 'SUCCESS',
                       'results': results}
        return jsonify(result_data)
    else:
        return jsonify({})


@app.before_request
def before_request():
    try:
        g.es = ElasticSearch(app.config['ELASTIC_SEARCH'])
    except:
        return jsonify({'status': 'ERROR'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
