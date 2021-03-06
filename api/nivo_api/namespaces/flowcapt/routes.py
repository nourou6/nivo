from datetime import timedelta, datetime
from json import JSONDecodeError
from urllib.parse import urlencode

import requests
from flask import jsonify
from flask_restx import Resource, abort

from nivo_api.core.api_schema.geojson import FeatureCollection
from nivo_api.core.db.connection import connection_scope
from nivo_api.core.db.models.sql.flowcapt import FlowCaptStationTable
from nivo_api.namespaces.flowcapt import flowcapt_api
from nivo_api.namespaces.flowcapt.models import FlowCaptRssToJSON
from nivo_api.settings import Config


@flowcapt_api.route("/stations")
class FlowCaptStationRessource(Resource):
    @flowcapt_api.response(200, "OK", FeatureCollection)
    def get(self):
        with connection_scope() as con:
            res = FlowCaptStationTable.get_geojson(con)
        return jsonify(res)


@flowcapt_api.route("/measures/<string:station_id>")
class FlowCaptMeasureResource(Resource):
    """
    ISAW does not respond to CORS. So proxying request to their website.
    """

    @flowcapt_api.response(200, "OK")
    @flowcapt_api.response("404", "Measure for this station_id cannot be found.")
    def get(self, station_id: str) -> dict:
        url = _build_query(station_id, 168)
        try:
            res = FlowCaptRssToJSON(url)
            return res()
        except JSONDecodeError:
            return abort(404, "Measure for this station_id cannot be found.")


@flowcapt_api.route("/measures/with_timestamp/<string:station_id>")
class FlowCaptMeasureWithTimestamp(Resource):
    @flowcapt_api.response(200, "OK")
    @flowcapt_api.response("404", "Measure for this station_id cannot be found.")
    def get(self, station_id: str) -> dict:
        url = _build_query(station_id, 168)
        try:
            res = requests.get(url).json()
            lastdata = datetime.strptime(res["lastdata"], "%Y-%m-%d %H:%M:%S")
            for k, values in res["measures"].items():
                res["measures"][k] = [
                    [v, (lastdata - timedelta(hours=idx)).timestamp()]
                    for idx, v in enumerate(values)
                ]
            return res
        except JSONDecodeError as e:
            return abort(404, "Measure for this station_id cannot be found.")


def _build_query(station: str, duration: int) -> str:
    url = Config.FLOWCAPT_MEASURE_URL
    qs = urlencode({"d": duration, "s": station, "f": "rss"})
    return f"{url}?{qs}"
