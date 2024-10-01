import pytz
from datetime import datetime, timedelta
from flask_restx import Namespace, Resource, fields
from .... import PyAutomation
from ....extensions.api import api
from ....extensions import _api as Api


ns = Namespace('Tags', description='Tags')
app = PyAutomation()

query_trends_model = api.model("query_trends_model",{
    'tags':  fields.List(fields.String(), required=True),
    'greater_than_timestamp': fields.DateTime(required=True, default=datetime.now().astimezone(pytz.UTC) - timedelta(minutes=5), description='Greater than DateTime'),
    'less_than_timestamp': fields.DateTime(required=True, default=datetime.now().astimezone(pytz.UTC), description='Less than DateTime'),
    'timezone': fields.String(required=True, default='UTC')
})


@ns.route('/')
class TagsCollection(Resource):

    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    def get(self):
        """
        Get Tags
        """
        return app.get_tags(), 200
    
@ns.route('/query_trends')
class QueryTrendsResource(Resource):

    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    @ns.expect(query_trends_model)
    def post(self):
        """
        Query tag value filtering by timestamp

        Authorized Roles: {0}
        """
        timezone = 'UTC'
        tags = api.payload['tags']
        if "timezone" in api.payload:

            timezone = api.payload["timezone"]

        if timezone not in pytz.all_timezones:

            return f"Invalid Timezone", 400
        
        separator = '.'
        greater_than_timestamp = api.payload['greater_than_timestamp']
        start = greater_than_timestamp.replace("T", " ").split(separator, 1)[0] + '.00'
        less_than_timestamp = api.payload['less_than_timestamp']
        stop = less_than_timestamp.replace("T", " ").split(separator, 1)[0] + '.00'
        result = app.get_trends(start, stop, timezone, *tags)
        
        return result, 200
    
@ns.route('/timezones')
class TimezonesCollection(Resource):

    @api.doc(security='apikey')
    @Api.token_required(auth=True)
    def get(self):
        """
        Get Available Timezones
        """
        return pytz.all_timezones, 200