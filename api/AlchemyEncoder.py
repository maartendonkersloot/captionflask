"""
Alchemy API Encoder to return json objects
Returns:
    [type]: The alchemyencoder class
"""
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    """
    Alchemy API Encoder class
    Args:
        json ([type]): json encocder
    """

    def default(self, o):
        """
        Default function to encode objects
        Args:
            obj ([type]): object to encode

        Returns:
            [type]: json object
        """
        if isinstance(o.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [
                x for x in dir(o) if not x.startswith("_") and x != "metadata"
            ]:
                data = o.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, o)
