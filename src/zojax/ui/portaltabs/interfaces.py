##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from z3c.schema.baseurl import BaseURL
from zope.i18nmessageid import MessageFactory

from zojax.richtext.field import RichText

_ = MessageFactory('zojax.ui.portaltabs')


class IPortalTabsLayer(interface.Interface):
    """ portal tabs layer """


class IPortalTab(interface.Interface):

    id = interface.Attribute('ID')

    url = interface.Attribute('Url')

    title = interface.Attribute('Title')
    
    description = interface.Attribute('Description')

    submenu = interface.Attribute('Submenu')

    configlet_title = interface.Attribute('Title for configlet')

    def __bind__(context, request):
        """ bind portal tab to context """

    def isSelected(strict=False):
        """ is tab selected """


class IBoundPortalTab(interface.Interface):
    """ marker interface for bound portal tab """


class IPortalTabsConfiglet(interface.Interface):
    """ portal tabs configuration """

    tabs = schema.List(
        title = _('Enabled portal tabs'),
        description = _(u'Select tabs that will be visible in portal tabs menu.'),
        value_type = schema.Choice(vocabulary = "portal.tabs"),
        default = [],
        required = False)

    registered = interface.Attribute('Registered persistent tabs')

    def getTab(tabId):
        """ return IPortalTab object """

    def getTabs(context, request):
        """ return enabled tabs for (context, request) """

    def registerTab(tab):
        """ register portal tab (IPortalTab object) """

    def unregisterTab(tab):
        """ unregister portal tab (IPortalTab object) """


class IPortalTabsExtension(interface.Interface):
    """ portal tabs extension """

    tabtitle = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Select title for portal tab.'),
        required = True)
    
    tabdescription = RichText(
        title = _(u'Description'),
        description = _(u'Select description for portal tab.'),
        required = False)

    enabled = schema.Bool(
        title = _(u'Enable'),
        description = _(u'Enable portal tab for this object.'),
        default = False,
        required = False)

    visible = schema.Bool(
        title = _(u'Visible'),
        description = _(u'Visible portal tab for this object.'),
        default = False,
        required = False)


class IPersistentPortalTab(IPortalTab):
    """ persistent portal tab """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Select title for portal tab.'),
        required = True)
    
    description = RichText(
        title = _(u'Description'),
        description = _(u'Select description for portal tab.'),
        required = False)

    submenu = schema.List(
        title = _('Submenu portal tabs'),
        description = _(u'Select tabs that will be visible as submenu.'),
        value_type = schema.Choice(vocabulary = "portal.topleveltabs"),
        default = [],
        required = False)

    def getSubmenu():
        """ return submenu tabs """


class ISimplePortalTab(IPersistentPortalTab):
    """ portal tab for object """

    url = schema.TextLine(
        title = _(u'URL'),
        description = _(u'Define url mapper for content.'),
        required = False)

    submenu = schema.List(
        title = _('Submenu portal tabs'),
        description = _(u'Select tabs that will be visible as submenu.'),
        value_type = schema.Choice(vocabulary = "portal.topleveltabs"),
        default = [],
        required = False)


class IObjectPortalTab(IPersistentPortalTab):
    """ portal tab for object """
