from flask import Flask, jsonify, json, Response, request
from github_scraper import scraper_users, scraper_repos

# Create the Flask app
app = Flask(__name__)
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# Define a route and a view function

@app.route('/users/<username>', methods = ['POST', 'GET'])
def getSpecificUser(username):    
    data = scraper_users(username)
    if type(data) is dict:
        return Response(json.dumps(data, sort_keys = False), mimetype= "application/json")
    else:
        return jsonify({"Error: user not found"}), 404

@app.route('/users/<username>/repos', methods = ['POST', 'GET'])
def getRepos(username):    
    sort = request.args.get('sort', default = 'full_name')
    per_page = request.args.get('per_page', default = 30)
    if sort == 'full_name':
        direction = request.args.get('direction', default='asc')
    else:
        direction = request.args.get('direction', default='desc')
    
    qpage = int(request.args.get('page', default = 1))

    
    data = scraper_repos(username, per_page=per_page, qpage=qpage)
    # print(type)
    if type(data) is not list:
        return jsonify({"Error: user not found"}), 404       
    else:  
        if per_page != 30:
            start = (qpage-1)*per_page
            end = start+per_page
            data = data[start:end]      
        if sort == "full_name":
            custom_key = lambda x: x['full_name']
            if direction == "asc":
                sorted_data = sorted(data, key=custom_key)
                return Response(json.dumps(sorted_data, sort_keys = False), mimetype= "application/json")
            else:
                sorted_data = sorted(data, key = custom_key, reverse=True)
                return Response(json.dumps(sorted_data, sort_keys = False), mimetype= "application/json")
        elif sort == "pushed":
            custom_key = lambda x: x['pushed_at']
            if direction == "asc":
                sorted_data = sorted(data, key=custom_key)
                return Response(json.dumps(sorted_data, sort_keys = False), mimetype= "application/json")
            else:
                sorted_data = sorted(data, key=custom_key, reverse=True)
                return Response(json.dumps(sorted_data, sort_keys = False), mimetype= "application/json")
            
@app.route('/users/<username>/repos', methods = ['POST', 'GET'])
def defaultResponse():
    return jsonify({"Error: user not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run()


