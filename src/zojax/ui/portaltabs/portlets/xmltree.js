menu = {
    version :"1.0"
};

// class menu.navigationTreeNode
menu.navigationTreeNode = function(menu, domNode) {
    this.childNodes = new Array();
    this.isEmpty = 1;
    this.isCollapsed = 1;
    this.domNode = domNode;
    this.loadingNode = null;
    this.path = '';
    this.parentNode = null;
    this.isRoot = 0;
    this.menu = menu
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

menu.navigationTreeNode.prototype.setSubSelected = function() {
    $(this.domNode).find('.icon').addClass('have-selected-subobject');
}

menu.navigationTreeNode.prototype.setSelected = function() {
    $(this.menu.navigationTree.domNode).find('.icon').removeClass('menutree-selected');
    $(this.domNode).find('.icon').addClass('menutree-selected');
    var parent = this.parentNode;
    while (parent) {
        parent.setSubSelected();
        parent = parent.parentNode
    }
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
    var expand = this.domNode.getElementsByTagName(this.menu.EXPAND)[0];
    //expand.style.backgroundImage = 'url("' + this.menu.baseurl + '@@/' + icon + '.gif")';
    expand.className= 'expand ' + icon
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

menu.MenuTree = function(id, rooturl, thismenubaseurl, fromtab, hidesliblings) {
    // constants
    this.ELEMENT_NODE = 1;
    this.TEXT_NODE = 3;
    this.COLLECTION = 'COLLECTION';
    this.ICON = 'DIV';
    this.EXPAND = 'DIV';
    this.XML_PUBLISHER_VIEW = 'zojax.ui.portaltabs'
    this.XML_CHILDREN_VIEW = '@@menuChildren.xml';
    this.SINGLE_BRANCH_TREE_VIEW = '@@menuSingleBranchTree.xml';
    this.CONTENT_VIEW = '@@SelectedManagementView.html';
    this.NUM_TEMPLATE = '$${num}';

    this.LG_DEBUG = 6;
    this.LG_TRACE_EVENTS = 5;
    this.LG_TRACE = 4;
    this.LG_INFO = 3;
    this.LG_NOLOG = 0;

    // globals
    this.loadingMsg = 'Loading...';
    this.abortMsg = 'Unavailable';
    this.titleTemplate = 'Contains ' + this.NUM_TEMPLATE + ' item(s)';
    this.navigationTree;
    this.loglevel = this.LG_NOLOG;
    
    this.baseurl = rooturl; // Global menu.baseurl
    this.docNavTree = document.getElementById(id);
    if (!this.docNavTree)
        return
    this.hideSiblings = hidesliblings;
    var url = thismenubaseurl + this.SINGLE_BRANCH_TREE_VIEW;
    if (fromtab) {
        url = this.XML_PUBLISHER_VIEW + '/' + fromtab + '/' + this.SINGLE_BRANCH_TREE_VIEW;
    }
    this.loadtreexml(url, null);

}

// utilities
menu.MenuTree.prototype.prettydump = function(s, locallog) {
    // Put the string "s" in a box on the screen as an log message
    if (locallog > menu.loglevel)
        return;

    var logger = document.getElementById('logger');
    var msg = document.createElement('code');
    var br1 = document.createElement('br');
    var br2 = document.createElement('br');
    var msg_text = document.createTextNode(s);
    msg.appendChild(msg_text);
    if (!logger) {
        return
    }
    logger.insertBefore(br1, logger.firstChild);
    logger.insertBefore(br2, logger.firstChild);
    logger.insertBefore(msg, logger.firstChild);
}

menu.MenuTree.prototype.debug = function(s) {
    var oldlevel = menu.loglevel;
    menu.loglevel = menu.LG_DEBUG;
    menu.prettydump("Debug : " + s, menu.LG_DEBUG);
    menu.loglevel = oldlevel;
}

// DOM utilities
menu.MenuTree.prototype.getTreeEventTarget = function(e) {
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

menu.MenuTree.prototype.isCollection = function(elem) {
    return this.checkTagName(elem, this.COLLECTION);
}

menu.MenuTree.prototype.isIcon = function(elem) {
    return this.checkTagName(elem, this.ICON);
}

menu.MenuTree.prototype.isExpand = function(elem) {
    return this.checkTagName(elem, this.EXPAND) && elem.className.search('expand') != -1;
}

menu.MenuTree.prototype.checkTagName = function(elem, tagName) {
    return elem.tagName.toUpperCase() == tagName;
}

menu.MenuTree.prototype.getCollectionChildNodes = function(xmlDomElem) {
    // get collection element nodes among childNodes of elem
    var result = new Array();

    var items = xmlDomElem.childNodes;
    var numitems = items.length;
    var currentItem;
    for ( var i = 0; i < numitems; i++) {
        currentItem = items[i];

        if (currentItem.nodeType == this.ELEMENT_NODE) {
            result.push(currentItem);
        }
    }
    return result;
}

// events
menu.MenuTree.prototype.treeclicked = function(e) {
    this.prettydump('menu.treeclicked', this.LG_TRACE_EVENTS);
    var elem = this.getTreeEventTarget(e);
    if (elem.id == 'menutree') {
        return
    }
    // if node clicked is expand elem, toggle expansion
    if (this.isExpand(elem) && !elem.getAttribute('empty')) {
        // get collection node
        elem = elem.parentNode;
        var navTreeNode = this.navigationTree.getNodeByPath(elem.getAttribute('path'));
        navTreeNode.toggleExpansion();
    }
}

menu.MenuTree.prototype.loadtreexml = function(url, node) {
    this.prettydump('URL ' + url, this.LG_INFO);
    var parseXML = this.parseXML;
    var instance = this;
    $.get(url, function(data) {
        parseXML(instance, data, node)
    });
}

menu.MenuTree.prototype.removeChildren = function(node) {
    var items = node.childNodes;
    var numitems = items.length;
    for ( var i = 0; i < numitems; i++) {
        node.removeChild(items[i]);
    }
}

menu.MenuTree.prototype.parseXML = function(instance, responseXML, node) {
    if (responseXML) {
        var data = responseXML.documentElement;
        if (node == null) {
            // [top] node
            instance.removeChildren(instance.docNavTree);
            instance.titleTemplate = data.getAttribute('title_tpl');
            instance.loadingMsg = data.getAttribute('loading_msg');
            instance.addNavigationTreeNodes(data, null, 1);
            // menu.docNavTree.appendChild(menu.navigationTree.domNode);
        } else {
            // expanding nodes
            instance.addNavigationTreeNodes(data, node, 0);
            node.finishLoadingChildren();
        }
    } else {
        // no XML response, reset the loadingNode
        if (node == null) {
            // unable to retrieve [top] node
            instance.docNavTree.innerHTML = this.abortMsg;
        } else {
            // abort expanding nodes
            node.abortLoadingChildren()
        }
    }
}

menu.MenuTree.prototype.addNavigationTreeNodes = function(sourceNode, targetNavTreeNode, deep) {
    // create tree nodes from XML children nodes of sourceNode
    // and add them to targetNode
    // if deep, create all descendants of sourceNode
    var basePath = "";
    var items = this.getCollectionChildNodes(sourceNode);
    var numitems = items.length;
    for ( var i = 0; i < numitems; i++) {
        var navTreeChild = this.createNavigationTreeNode(items[i], basePath,
                deep);
        if (targetNavTreeNode)
            targetNavTreeNode.appendChild(navTreeChild);
    }
}

menu.MenuTree.prototype.createPresentationNodes = function(title, targetUrl, icon_url, length) {
    // create nodes hierarchy for one collection (without children)

    // create elem for plus/minus icon
    var expandElem = document.createElement(this.EXPAND);
    expandElem.className = 'expand'
    var instance = this;
    $(expandElem).click(function (e) {
        instance.treeclicked(e)
    });
    // create elem for item icon
    var iconElem = document.createElement(this.ICON);
    iconElem.className = 'icon';
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
        var titleText = this.titleTemplate.split(this.NUM_TEMPLATE).join(length);
        linkElem.setAttribute('title', title);
        linkElem.setAttribute('href', targetUrl);
    }
    else {
        linkElem = document.createElement('span');
        var titleTextNode = document.createTextNode(title);

        linkElem.appendChild(titleTextNode);
        var titleText = this.titleTemplate.split(this.NUM_TEMPLATE).join(length);
        linkElem.setAttribute('title', title);
    }
    iconElem.appendChild(linkElem);

    return expandElem;
}

menu.MenuTree.prototype.createLoadingNode = function() {
    var loadingElem = document.createElement('loading');
    var titleTextNode = document.createTextNode(this.loadingMsg);

    loadingElem.appendChild(titleTextNode);

    return loadingElem;
}

menu.MenuTree.prototype.createNavigationTreeNode = function(source, basePath, deep) {
    var newelem = document.createElement('div');
    newelem.className = 'collection'
    var navTreeNode = new menu.navigationTreeNode(this, newelem);
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
        this.navigationTree = navTreeNode;
        navTreeNode.setIsRoot(1);
        this.docNavTree.appendChild(newelem);
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
        var expandElem = this.createPresentationNodes(elemTitle, targetUrl,
                icon_url, length);
        newelem.appendChild(expandElem);
        // If no child element, we can disable the tree expansion
        if (length == '0' || !length)
            expandElem.setAttribute('empty', '1');
    }
    
    var selected = source.getAttribute('selected')=='1';

    if (deep) {
        var children = this.getCollectionChildNodes(source);
        var numchildren = children.length;
        for ( var i = 0; i < numchildren; i++) {
            var navTreeNodeChild = this.createNavigationTreeNode(children[i],
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

    // If this is the selected node, we want to highlight it with CSS
    if (selected)
        navTreeNode.setSelected();

    return navTreeNode;
}
