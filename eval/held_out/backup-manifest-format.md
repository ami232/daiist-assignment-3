# Manifest-Checksum

This key is always present on the last line of the backup manifest file. The associated value is a SHA256 checksum of all the preceding lines. We use a fixed checksum method here to make it possible for clients to do incremental parsing of the manifest. While a SHA256 checksum is significantly more expensive than a CRC32C checksum, the manifest should normally be small enough that the extra computation won't matter very much.

PostgreSQL 17.12, Backup Manifest Format.
https://github.com/postgres/postgres/blob/REL_17_12/doc/src/sgml/backup-manifest.sgml#L86

Distributed under POSTGRESQL-LICENSE.txt.
