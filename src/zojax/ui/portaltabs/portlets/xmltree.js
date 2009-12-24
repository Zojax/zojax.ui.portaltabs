menu = {
    version :"1.0"
};

// constants
menu.ELEMENT_NODE = 1;
menu.TEXT_NODE = 3;
menu.COLLECTION = 'COLLECTION';
menu.ICON = 'ICON';
menu.EXPAND = 'EXPAND';
menu.XML_PUBLISHER_VIEW = 'zojax.ui.portaltabs'
menu.XML_CHILDREN_VIEW = '@@menuChildren.xml';
menu.SINGLE_BRANCH_TREE_VIEW = '@@menuSingleBranchTree.xml';
menu.CONTENT_VIEW = '@@SelectedManagementView.html';
menu.NUM_TEMPLATE = '$${num}';

menu.LG_DEBUG = 6;
menu.LG_TRACE_EVENTS = 5;
menu.LG_TRACE = 4;
menu.LG_INFO = 3;
menu.LG_NOLOG = 0;

// globals
menu.loadingMsg = 'Loading...';
menu.abortMsg = 'Unavailable';
menu.titleTemplate = 'Contains ' + menu.NUM_TEMPLATE + ' item(s)';
menu.baseurl;
menu.navigationTree;
menu.docNavTree;
menu.loglevel = menu.LG_NOLOG;
menu.hideSiblings = 0;

// class menu.navigationTreeNode
menu.navigationTreeNode = function(domNode) {
    this.childNodes = new Array();
    this.isEmpty = 1;
    this.isCollapsed = 1;
    this.domNode = domNode;
    this.loadingNode = null;
    this.path = '';
    this.parentNode = null;
    this.isRoot = 0;
}

menu.navigationTreeNode.prototype.appendChild = function(node) {
    this.childNodes.push(node);
    this.domNode.appendChild(node.domNode);
    node.parentNode = this;
}

menu.navigationTreeNode.prototype.setPath = function(path) {
    this.path = path;
    this.domNode.setAttribute("path", path);
}

menu.navigationTreeNode.prototype.setIsRoot = function(isRoot) {
    this.isRoot = isRoot;
    this.domNode.setAttribute("isRoot", isRoot);
}

menu.navigationTreeNode.prototype.setSelected = function() {
    var items = menu.navigationTree.domNode.getElementsByTagName('icon')
    for ( var i = 0; i < items.length; i++) {
        items[i].className = '';
    }
    this.domNode.getElementsByTagName('icon')[0].className = 'selected';
}

menu.navigationTreeNode.prototype.collapse = function() {
    this.isCollapsed = 1;
    this.changeExpandIcon("plus");
}

menu.navigationTreeNode.prototype.expand = function() {
    this.isCollapsed = 0;
    if (!this.isRoot)
        this.changeExpandIcon("minus");
}

menu.navigationTreeNode.prototype.changeExpandIcon = function(icon) {
    var expand = this.domNode.getElementsByTagName('expand')[0];
    expand.style.backgroundImage = 'url("' + menu.baseurl + '@@/' + icon + '.gif")';
    expand.className= icon
}

menu.navigationTreeNode.prototype.getNodeByPath = function(path) {
    var numchildren = this.childNodes.length;
    if (path == this.path)
        return this;
    else {
        for ( var i = 0; i < numchildren; i++) {
            foundChild = this.childNodes[i].getNodeByPath(path);
            if (foundChild)
                return foundChild;
        }
    }
    return null;
}

menu.navigationTreeNode.prototype.toggleExpansion = function() {
    with (this) {
        menu.prettydump('toggleExpansion', menu.LG_TRACE);
        // If this collection is empty, load it from server
        // todo xxx optimize for the case where collection has null length
        if (isEmpty)
            startLoadingChildren();
        else
            refreshExpansion();
        if (menu.hideSiblings && parentNode && parentNode.childNodes.length)
            for ( var i = 0; i < parentNode.childNodes.length; i++) {
                if (parentNode.childNodes[i].path != path &&
                        !parentNode.childNodes[i].isCollapsed)
                    parentNode.childNodes[i].refreshExpansion()
            }
    }
}

menu.navigationTreeNode.prototype.startLoadingChildren = function() {
    with (this) {
        // already loading?
        if (loadingNode)
            return;
        loadingNode = menu.createLoadingNode();
        domNode.appendChild(loadingNode);
        // var url = menu.baseurl + path + menu.XML_CHILDREN_VIEW;
        var url = menu.XML_PUBLISHER_VIEW + '/' + path + menu.XML_CHILDREN_VIEW;
        menu.loadtreexml(url, this);
    }
}

menu.navigationTreeNode.prototype.finishLoadingChildren = function() {
    with (this) {
        isEmpty = 0;
        refreshExpansion();
        domNode.removeChild(loadingNode);
        loadingNode = null;
    }
}

menu.navigationTreeNode.prototype.abortLoadingChildren = function() {
    with (this) {
        domNode.removeChild(loadingNode);
        loadingNode = null;
    }
}

menu.navigationTreeNode.prototype.refreshExpansion = function() {
    with (this) {
        if (isCollapsed) {
            expand();
            showChildren();
        } else {
            collapse();
            hideChildren();
        }
    }
}

menu.navigationTreeNode.prototype.hideChildren = function() {
    with (this) {
        menu.prettydump('hideChildren', menu.LG_TRACE);
        var num = childNodes.length;
        for ( var i = num - 1; i >= 0; i--) {
            childNodes[i].domNode.style.display = 'none';
        }
    }
}

menu.navigationTreeNode.prototype.showChildren = function() {
    with (this) {
        menu.prettydump('showChildren', menu.LG_TRACE);
        var num = childNodes.length;
        for ( var i = num - 1; i >= 0; i--) {
            childNodes[i].domNode.style.display = 'block';
        }
    }
}

// utilities
menu.prettydump = function(s, locallog) {
    // Put the string "s" in a box on the screen as an log message
    if (locallog > menu.loglevel)
        return;

    var logger = document.getElementById('logger');
    var msg = document.createElement('code');
    var br1 = document.createElement('br');
    var br2 = document.createElement('br');
    var msg_text = document.createTextNode(s);
    msg.appendChild(msg_text);
    logger.insertBefore(br1, logger.firstChild);
    logger.insertBefore(br2, logger.firstChild);
    logger.insertBefore(msg, logger.firstChild);
}

menu.debug = function(s) {
    var oldlevel = menu.loglevel;
    menu.loglevel = menu.LG_DEBUG;
    menu.prettydump("Debug : " + s, menu.LG_DEBUG);
    menu.loglevel = oldlevel;
}

// DOM utilities
menu.getTreeEventTarget = function(e) {
    var elem;
    if (e.target) {
        // Mozilla uses this
        if (e.target.nodeType == menu.TEXT_NODE) {
            elem = e.target.parentNode;
        } else
            elem = e.target;
    } else {
        // IE uses this
        elem = e.srcElement;
    }
    return elem;
}

menu.isCollection = function(elem) {
    return menu.checkTagName(elem, menu.COLLECTION);
}

menu.isIcon = function(elem) {
    return menu.checkTagName(elem, menu.ICON);
}

menu.isExpand = function(elem) {
    return menu.checkTagName(elem, menu.EXPAND);
}

menu.checkTagName = function(elem, tagName) {
    return elem.tagName.toUpperCase() == tagName;
}

menu.getCollectionChildNodes = function(xmlDomElem) {
    // get collection element nodes among childNodes of elem
    var result = new Array();

    var items = xmlDomElem.childNodes;
    var numitems = items.length;
    var currentItem;
    for ( var i = 0; i < numitems; i++) {
        currentItem = items[i];

        if (currentItem.nodeType == menu.ELEMENT_NODE) {
            result.push(currentItem);
        }
    }
    return result;
}

// events
menu.treeclicked = function(e) {
    menu.prettydump('menu.treeclicked', menu.LG_TRACE_EVENTS);
    var elem = menu.getTreeEventTarget(e);
    if (elem.id == 'menutree')
        return;

    // if node clicked is expand elem, toggle expansion
    if (menu.isExpand(elem) && !elem.getAttribute('disabled')) {
        // get collection node
        elem = elem.parentNode;
        var navTreeNode = menu.navigationTree.getNodeByPath(elem
                .getAttribute('path'));
        navTreeNode.toggleExpansion();
    }
}

// helpers
menu.getControlPrefix = function() {
    if (menu.getControlPrefix.prefix)
        return menu.getControlPrefix.prefix;

    var prefixes = [ "MSXML2", "Microsoft", "MSXML", "MSXML3" ];
    var o, o2;
    for ( var i = 0; i < prefixes.length; i++) {
        try {
            // try to create the objects
            o = new ActiveXObject(prefixes[i] + ".menu.XmlHttp");
            o2 = new ActiveXObject(prefixes[i] + ".XmlDom");
            return menu.getControlPrefix.prefix = prefixes[i];
        } catch (ex) {
        }
        ;
    }

    throw new Error("Could not find an installed XML parser");
}

// menu.XmlHttp factory
menu.XmlHttp = function() {
}

menu.XmlHttp.create = function() {
    if (window.XMLHttpRequest) {
        var req = new XMLHttpRequest();

        // some older versions of Moz did not support the readyState property
        // and the onreadystate event so we patch it!
        if (req.readyState == null) {
            req.readyState = 1;
            req.addEventListener("load", function() {
                req.readyState = 4;
                if (typeof req.onreadystatechange == "function")
                    req.onreadystatechange();
            }, false);
        }

        return req;
    }
    if (window.ActiveXObject) {
        s = menu.getControlPrefix() + '.menu.XmlHttp';
        return new ActiveXObject(menu.getControlPrefix() + ".menu.XmlHttp");
    }
    return;
};

menu.loadtreexml = function(url, node, fromtab) {
    var xmlHttp = menu.XmlHttp.create();
    if (!xmlHttp)
        return;
    menu.prettydump('URL ' + url, menu.LG_INFO);
    xmlHttp.open('GET', url, true);

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState != 4)
            return;
        menu.prettydump('Response XML ' + xmlHttp.responseText, menu.LG_INFO);
        menu.parseXML(xmlHttp.responseXML, node, fromtab);
    };

    // call in new thread to allow ui to update
    window.setTimeout( function() {
        xmlHttp.send(null);
    }, 10);
}

menu.loadtree = function(rooturl, thismenubaseurl, fromtab, hidesliblings) {
    menu.baseurl = rooturl; // Global menu.baseurl
    menu.docNavTree = document.getElementById('menutreecontents');
    menu.hideSiblings = hidesliblings;
    var url = thismenubaseurl + menu.SINGLE_BRANCH_TREE_VIEW;
    if (fromtab) {
        url = menu.XML_PUBLISHER_VIEW + '/' + fromtab + '/' + menu.SINGLE_BRANCH_TREE_VIEW;
    }
    menu.loadtreexml(url, null, fromtab);

}

menu.removeChildren = function(node) {
    var items = node.childNodes;
    var numitems = items.length;
    for ( var i = 0; i < numitems; i++) {
        node.removeChild(items[i]);
    }
}

menu.parseXML = function(responseXML, node) {
    if (responseXML) {
        var data = responseXML.documentElement;
        if (node == null) {
            // [top] node
            menu.removeChildren(menu.docNavTree);
            menu.titleTemplate = data.getAttribute('title_tpl');
            menu.loadingMsg = data.getAttribute('loading_msg');
            menu.addNavigationTreeNodes(data, null, 1);
            // menu.docNavTree.appendChild(menu.navigationTree.domNode);
        } else {
            // expanding nodes
            menu.addNavigationTreeNodes(data, node, 0);
            node.finishLoadingChildren();
        }
    } else {
        // no XML response, reset the loadingNode
        if (node == null) {
            // unable to retrieve [top] node
            menu.docNavTree.innerHTML = menu.abortMsg;
        } else {
            // abort expanding nodes
            node.abortLoadingChildren()
        }
    }
}

menu.addNavigationTreeNodes = function(sourceNode, targetNavTreeNode, deep) {
    // create tree nodes from XML children nodes of sourceNode
    // and add them to targetNode
    // if deep, create all descendants of sourceNode
    var basePath = "";
    var items = menu.getCollectionChildNodes(sourceNode);
    var numitems = items.length;
    for ( var i = 0; i < numitems; i++) {
        var navTreeChild = menu.createNavigationTreeNode(items[i], basePath,
                deep);
        if (targetNavTreeNode)
            targetNavTreeNode.appendChild(navTreeChild);
    }
}

menu.createPresentationNodes = function(title, targetUrl, icon_url, length) {
    // create nodes hierarchy for one collection (without children)

    // create elem for plus/minus icon
    var expandElem = document.createElement('expand');
    // create elem for item icon
    var iconElem = document.createElement('icon');
    expandElem.appendChild(iconElem);
    // Mozilla tries to infer an URL if url is empty and reloads containing page
    if (icon_url != '') {
        iconElem.style.backgroundImage = 'url("' + icon_url + '")';
    }
    var linkElem;
    if (targetUrl) {
    // create link
        linkElem = document.createElement('a');
        var titleTextNode = document.createTextNode(title);

        linkElem.appendChild(titleTextNode);
        var titleText = menu.titleTemplate.split(menu.NUM_TEMPLATE).join(length);
        linkElem.setAttribute('title', title);
        linkElem.setAttribute('href', targetUrl);
    }
    else {
        linkElem = document.createElement('span');
        var titleTextNode = document.createTextNode(title);

        linkElem.appendChild(titleTextNode);
        var titleText = menu.titleTemplate.split(menu.NUM_TEMPLATE).join(length);
        linkElem.setAttribute('title', title);
    }
    iconElem.appendChild(linkElem);

    return expandElem;
}

menu.createLoadingNode = function() {
    var loadingElem = document.createElement('loading');
    var titleTextNode = document.createTextNode(menu.loadingMsg);

    loadingElem.appendChild(titleTextNode);

    return loadingElem;
}

menu.createNavigationTreeNode = function(source, basePath, deep) {
    var newelem = document.createElement(source.tagName);

    var navTreeNode = new menu.navigationTreeNode(newelem);
    var elemPath;
    var elemTitle;
    var elemUrl;
    if (source.getAttribute('isroot') != null)  {
        // elemTitle = source.getAttribute('name');
        // elemPath = basePath;
        // set base url for virtual host support
        // menu.baseurl = source.getAttribute('baseURL');
        // elemPath = source.getAttribute('baseURL');
        newelem.style.marginLeft = '0px';
        menu.navigationTree = navTreeNode;
        navTreeNode.setIsRoot(1);
        menu.docNavTree.appendChild(newelem);
    } else {
        elemTitle = source.getAttribute('title');
        elemPath = basePath + source.getAttribute('name') + '/';
        elemUrl = source.getAttribute('url');
    }
    navTreeNode.setPath(elemPath);

    // could show number of child items
    var length = source.getAttribute('length');

    var icon_url = source.getAttribute('icon_url');

    var targetUrl = elemUrl;
    if (!navTreeNode.isRoot) {
        var expandElem = menu.createPresentationNodes(elemTitle, targetUrl,
                icon_url, length);
        newelem.appendChild(expandElem);
        // If no child element, we can disable the tree expansion
        if (length == '0' || !length)
            expandElem.setAttribute('disabled', '1');
    }
    // If this is the selected node, we want to highlight it with CSS
    if (source.getAttribute('selected')=='1')
        navTreeNode.setSelected();

    if (deep) {
        var children = menu.getCollectionChildNodes(source);
        var numchildren = children.length;
        for ( var i = 0; i < numchildren; i++) {
            var navTreeNodeChild = menu.createNavigationTreeNode(children[i],
                    basePath, deep);
            navTreeNode.appendChild(navTreeNodeChild);
        }
        if (numchildren) {
            navTreeNode.isEmpty = 0;
            navTreeNode.expand();
        } else {
            navTreeNode.isEmpty = 1;
            // if no child, we do not display icon '+'
            if (length != '0')
                navTreeNode.collapse();
        }
    } else {
        navTreeNode.isEmpty = 1;
        // if no child, we do not display icon '+'
        if (length != '0')
            navTreeNode.collapse();
    }
    return navTreeNode;
}
