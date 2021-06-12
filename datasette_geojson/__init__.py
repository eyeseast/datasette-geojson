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


async def render_geojson(datasette, columns, rows, request, database):
    if not can_render_geojson(datasette, columns):
        from datasette.views.base import DatasetteError

        raise DatasetteError("SQL query must include a geometry column")

    db = datasette.get_database(database)
    newline = bool(request.args.get("_nl", False))
    features = [await row_to_geojson(row, db) for row in rows]

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


async def row_to_geojson(row, db):
    "Turn a row with a geometry column into a geojson feature"
    row = dict(row)
    geometry = await parse_geometry(row.pop("geometry"), db)

    return geojson.Feature(geometry=geometry, properties=row)


async def parse_geometry(geometry, db):
    "Start with a string, or binary blob, or dict, and return a geometry dict"
    if isinstance(geometry, dict):
        return geometry

    if isinstance(geometry, str):
        return geojson.loads(geometry)

    if isinstance(geometry, bytes):
        results = await db.execute(
            "SELECT AsGeoJSON(:geometry)", {"geometry": geometry}
        )

        return geojson.loads(results.single_value())

    raise ValueError(f"Unexpected geometry type: {type(geometry)}")
