"""This contains the IMAGE property from :rfc:`7986`."""

from __future__ import annotations

from typing import TYPE_CHECKING

from icalendar.prop.binary import vBinary
from icalendar.prop.uri import vUri

if TYPE_CHECKING:
    from icalendar.prop.text import vText


class Image:
    """An image as URI or BINARY according to :rfc:`7986`.

    The value must be a URI or binary data with a media type of "image" or
    refer to such data.

    This property specifies an image for an iCalendar object or a calendar
    component via a URI or directly with inline data that can be used by
    calendar user agents when presenting the calendar data to a user.

    Parameters:
        altrep: Link target of the image.
        b64data: The data of the image, base64 encoded.
        display: The display mode, for example, ``"BADGE"``.
        fmttype: The format type, for example, ``"image/png"``.
        uri: The URI of the image.

    """

    @classmethod
    def from_property_value(cls, value: vUri | vBinary | vText) -> Image:
        """Create an Image from a property value."""
        params: dict[str, str] = {}
        if not hasattr(value, "params"):
            raise TypeError("Value must be URI or BINARY.")
        try:
            value_type = value.params.get("VALUE", "").upper()
        except (AttributeError, TypeError) as err:
            raise TypeError("Value must have a valid params attribute.") from err
        if value_type == "URI" or isinstance(value, vUri):
            params["uri"] = str(value)
        elif isinstance(value, vBinary):
            params["b64data"] = value.base64data
        elif value_type == "BINARY":
            params["b64data"] = str(value)
        else:
            raise TypeError(
                f"The VALUE parameter must be URI or BINARY, not {value_type!r}."
            )
        params.update(
            {
                "fmttype": value.params.get("FMTTYPE"),
                "altrep": value.params.get("ALTREP"),
                "display": value.params.get("DISPLAY"),
            }
        )
        return cls(**params)

    def __init__(
        self,
        uri: str | None = None,
        b64data: str | None = None,
        fmttype: str | None = None,
        altrep: str | None = None,
        display: str | None = None,
    ) -> None:
        if uri is not None and b64data is not None:
            raise ValueError("Image cannot have both URI and binary data (RFC 7986)")
        if uri is None and b64data is None:
            raise ValueError("Image must have either URI or binary data")
        self.uri = uri
        self.b64data = b64data
        self.fmttype = fmttype
        self.altrep = altrep
        self.display = display

    @property
    def data(self) -> bytes | None:
        """Return the binary data, if available."""
        if self.b64data is None:
            return None
        return vBinary.from_ical(self.b64data)


__all__ = ["Image"]
