import json
import geojson
from datasette import hookimpl
from datasette.utils.asgi import Response


@hookimpl
def register_output_renderer(datasette):
    return {
        "extension": "geojson",
        "render": render_geojson,
        "can_render": can_render_geojson,
    }


def render_geojson(datasette, columns, rows, request):
    if not can_render_geojson(datasette, columns):
        from datasette.views.base import DatasetteError

        raise DatasetteError("SQL query must include a geometry column")

    newline = bool(request.args.get("_nl", False))
    features = [row_to_geojson(row) for row in rows]

    if newline:
        # todo: stream this
        lines = [json.dumps(feature) for feature in features]
        return Response.text("\n".join(lines))

    fc = geojson.FeatureCollection(features=features)
    return Response.json(dict(fc))


def can_render_geojson(datasette, columns):
    """
    Check if there's a geometry column
    """
    return "geometry" in columns


def row_to_geojson(row):
    "Turn a row with a geometry column into a geojson feature"
    row = dict(row)
    geometry = parse_geometry(row.pop("geometry"))

    return geojson.Feature(geometry=geometry, properties=row)


def parse_geometry(geometry):
    "Start with a string, or binary blob, or dict, and return a geometry dict"
    if isinstance(geometry, dict):
        return geometry

    if isinstance(geometry, str):
        return geojson.loads(geometry)

    if isinstance(geometry, bytes):
        raise ValueError("Can't parse geometry blob")

    raise ValueError("Unknown type")
