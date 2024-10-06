==========================
Disable Filestore Errors
==========================

Overview
========

The **Disable Filestore Errors** module is designed to handle missing files in Odoo's filestore gracefully, which is particularly useful in development environments.

When restoring a database backup without the corresponding filestore, Odoo often throws `FileNotFoundError` or `CacheMiss` errors during operation, cluttering the logs with tracebacks and interrupting development. This module prevents these issues by logging a warning and returning empty content instead of raising an exception.
