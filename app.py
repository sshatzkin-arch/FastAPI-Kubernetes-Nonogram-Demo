from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, reqparse
from flask_swagger import swagger

app = Flask(__name__)
api = Api(app)

STUDENTS = {
  '1': {'name': 'Mark', 'age': 23, 'spec': 'math'},
  '2': {'name': 'Jane', 'age': 20, 'spec': 'biology'},
  '3': {'name': 'Peter', 'age': 21, 'spec': 'history'},
  '4': {'name': 'Kate', 'age': 22, 'spec': 'science'},
  '5': {'name': 'Steve', 'age': 19, 'spec': 'english'}
}

if __name__ == "__main__":
  app.run(debug=True)



class StudentsList(Resource):
  def get(self):
    return STUDENTS

  parser = reqparse.RequestParser()

  def post(self):
    parser.add_argument("name")
    parser.add_argument("age")
    parser.add_argument("spec")
    args = parser.parse_args()
    student_id = int(max(STUDENTS.keys())) + 1
    student_id = '%i' % student_id
    STUDENTS[student_id] = {
      "name": args["name"],
      "age": args["age"],
      "spec": args["spec"],
    }
    return STUDENTS[student_id], 201


api.add_resource(StudentsList, '/students/')

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()

@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "2.0"
    swag['info']['title'] = "Test Api"
    swag['host'] = "http://localhost:5000"
    swag['basePath'] = ""
    swag['schemes'] = ['https']
    swag['paths'] = \
      {'/students':
        {'get':
          {'summary': 'Returns a list of the students.',
          'parameters':'None',
          'produces':['application/json'],
          'responses':
            {'200':{'description':'OK'},
             '400':{'description':'Invalid Something'}
             }
          }
         }
      }
    return jsonify(swag)