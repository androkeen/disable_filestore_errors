# Stdlib:
import logging
import os

# Odoo:
from odoo import models
from odoo.http import Stream

_logger = logging.getLogger(__name__)


# Patch the Stream class to handle missing files gracefully
class StreamPatched(Stream):
    @classmethod
    def from_attachment(cls, attachment):
        """Override to handle missing file gracefully."""
        try:
            # Try accessing the file
            if not attachment.path or not os.path.exists(attachment.path):
                # If the file does not exist, log and return an empty stream
                _logger.warning("Attachment file not found: %s. Returning empty content.", attachment.path)
                return cls(type="data", data=b"", size=0)

            # If the file exists, proceed as normal
            os.stat(attachment.path)
            return super().from_attachment(attachment)

        except FileNotFoundError:
            # Handle missing file case gracefully
            _logger.warning("Attachment file not found: %s. Returning empty content.", attachment.path)
            return cls(type="data", data=b"", size=0)  # Return an empty stream

        except OSError as e:
            # Handle other I/O errors gracefully
            _logger.error("Error accessing attachment file %s: %s", attachment.path, e, exc_info=True)
            return cls(type="data", data=b"", size=0)  # Return an empty stream


class IrBinary(models.AbstractModel):
    _inherit = "ir.binary"

    def _record_to_stream(self, record, field_name):
        """
        Override the method to handle FileNotFoundError gracefully and avoid breaking
        the request when files are missing in the filestore.
        """
        try:
            # Attempt to retrieve the stream as usual
            return super()._record_to_stream(record, field_name)
        except FileNotFoundError:
            # Handle the case where the file is missing in the filestore
            _logger.warning("File not found for record %s in field %s. Returning an empty stream.", record, field_name)
            return StreamPatched(type="data", data=b"", size=0)
        except OSError:
            # Handle other file system-related errors gracefully
            _logger.warning("Error accessing file for record %s in field %s.", record, field_name, exc_info=True)
            return StreamPatched(type="data", data=b"", size=0)
