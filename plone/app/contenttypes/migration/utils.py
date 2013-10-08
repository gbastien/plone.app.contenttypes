# -*- coding: utf-8 -*-
import pkg_resources
from zope.component import getGlobalSiteManager

from Products.ATContentTypes.interfaces.document import IATDocument
from Products.ATContentTypes.interfaces.file import IATFile
from Products.ATContentTypes.interfaces.folder import IATFolder
from Products.ATContentTypes.interfaces.image import IATImage
from Products.ATContentTypes.interfaces.link import IATLink
from Products.ATContentTypes.interfaces.news import IATNewsItem
from plone.app.blob.interfaces import IATBlobImage
from plone.app.blob.interfaces import IATBlobFile

# Schema Extender allowed interfaces
from archetypes.schemaextender.interfaces import (
    ISchemaExtender,
    IOrderableSchemaExtender,
    IBrowserLayerAwareExtender,
    ISchemaModifier
)

try:
    pkg_resources.get_distribution('plone.app.collection')
except pkg_resources.DistributionNotFound:
    ICollection = None
    HAS_APP_COLLECTION = False
else:
    HAS_APP_COLLECTION = True
    from plone.app.collection.interfaces import ICollection

from plone.app.contenttypes.migration import migration

ATCT_LIST = {
    "Folder": {
        'iface': IATFolder,
        'migrator': migration.migrate_folders,
        'extended_fields': [],
    },
    "Document": {
        'iface': IATDocument,
        'migrator': migration.migrate_documents,
        'extended_fields': [],
    },
    "File": {
        'iface': IATFile,
        'migrator': migration.migrate_files,
        'extended_fields': [],
    },
    "Image": {
        'iface': IATImage,
        'migrator': migration.migrate_images,
        'extended_fields': [],
    },
    "News Item": {
        'iface': IATNewsItem,
        'migrator': migration.migrate_newsitems,
        'extended_fields': [],
    },
    "Link": {
        'iface': IATLink,
        'migrator': migration.migrate_links,
        'extended_fields': [],
    },
    "BlobImage": {
        'iface': IATBlobImage,
        'migrator': migration.migrate_blobimages,
        'extended_fields': ['image'],
    },
    "BlobFile": {
        'iface': IATBlobFile,
        'migrator': migration.migrate_blobfiles,
        'extended_fields': ['file'],
    },
}

if HAS_APP_COLLECTION:
    ATCT_LIST["Collection"] = {
        'iface': ICollection,
        'migrator': migration.migrate_collections,
        'extended_fields': [],
    }


def isSchemaExtended(interface):
    """Return whether a specific content type interface
    is extended by archetypes.schemaextender or not
    """
    sm = getGlobalSiteManager()
    extender_interfaces = [
        ISchemaExtender,
        ISchemaModifier,
        IBrowserLayerAwareExtender,
        IOrderableSchemaExtender,
    ]
    # We have a few possible interfaces to test
    # here, so get all the interfaces that
    # are for the given content type first
    registrations = \
        [a for a in sm.registeredAdapters() if interface in a.required]
    for adapter in registrations:
        if adapter.provided in extender_interfaces:
            fields = adapter.factory(None).fields
            return [field.getName() for field in fields]
    return []
