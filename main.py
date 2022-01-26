from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from ariadne import load_schema_from_path
from flask import Flask, request, jsonify
from lambda_function import lambda_handler

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()


# Define resolver
@query.field("getInternalUser")
def get_internal_user(*_, auth0UserId):
    data = {
        "input": {
            "auth0UserId": auth0UserId
        }
    }
    return lambda_handler(data)


schema = make_executable_schema(type_defs, query)

app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
       schema,
       data,
       context_value={
           "request": request
       }
    )
    status_code = 200 if success else 400

    return jsonify(result), status_code


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
