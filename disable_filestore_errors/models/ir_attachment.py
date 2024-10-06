# Stdlib:
import logging

# Odoo:
from odoo import models

_logger = logging.getLogger(__name__)


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    def _file_read(self, fname):
        """Override to handle missing file gracefully."""
        full_path = self._full_path(fname)
        try:
            with open(full_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            # Log a warning instead of raising the error
            _logger.warning("File not found: %s. Returning empty content.", full_path)
            return b""  # Return empty byte content if the file is not found
        except OSError as e:
            # Log other file access errors
            _logger.error("Error reading file %s: %s", full_path, e)
            return b""
