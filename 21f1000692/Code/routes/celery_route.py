from flask_restful import Resource
from flask import jsonify, request, make_response


class dailyMail(Resource):
    def get(self):
        from tasks import ex_daily
        var2 = ex_daily.delay()
        while not var2.ready():
            pass
        return make_response(jsonify({"message": "task triggered successfully", "id": var2.id, "name": var2.result, "status": var2.status}), 201)
        