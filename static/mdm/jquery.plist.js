(function ( $ ) {
    var tableElement;
    var defaultOptions = {
      protect: 0
    };

    $.fn.loadPropertyList = function( xml, options )
    {
        try {
	    var plist, plist_data, rows, root, opt;

            opt = $.extend(defaultOptions, options);

            // Clear any existing data.
	    $(this).empty();
	    $(this).append('<table class="plist"></table>');

	    plist = $(xml).children().eq(0);
	    if (plist.get(0).nodeName == 'plist')
                root = plist.children().eq(0);
            else if (plist.get(0).nodeName == 'dict' || plist.get(0).nodeName == 'array')
                root = plist.children().eq(0);
            else
		return false;

	    plist_data = parsePropertyListNode(root);
	    plist_data['key'] = 'Root';
	    rows = generatePlistDOM([ plist_data ], 0, false, opt);
	    $(this).children('table').eq(0).append(rows);
	}
	catch (err) {
	    return false;
	}

	return true;
    };

    $.fn.emptyPropertyList = function( options )
    {
        try {
	    var plist, plist_data, rows;

            // Clear any existing data.
            $(this).empty();
            $(this).append('<table class="plist"></table>');

	    plist_data = parsePropertyListNode($('<dict></dict>'));
	    plist_data['key'] = 'Root';
	    rows = generatePlistDOM([ plist_data ], 0, false);
	    $(this).children('table').eq(0).append(rows);
	}
	catch (err) {
	    return false;
	}

	return true;
    };

    $.fn.savePropertyList = function()
    {
        var text = '';

	try {
	    var rows = $(this).find('table > tbody > tr');
	    var recurse = processSaveLevel(rows, 0, 0);

	    text += '<?xml version="1.0" encoding="UTF-8"?>\n';
	    text += '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n';
	    text += '<plist version="1.0">\n';
	    text += recurse.text;
	    text += '</plist>\n';
	}
	catch (err) {
	    return false;
	}

	return text;
    }

    var entityMap = {
	"&": "&amp;",
	"<": "&lt;",
	">": "&gt;",
	'"': '&quot;',
	"'": '&#39;'
    };

    function escapeXml(string) {
	return String(string).replace(/[&<>"']/g, function (s) {
	    return entityMap[s];
	});
    }

    function generatePlistDOM(plist, level, readonlykey, options)
    {
	var rows = [ ];
	var idx = 0;

	for (var i = 0; i < plist.length; i++) {
	    var item = plist[i];
	    var key = item.key;
	    var row = $('<tr data-indentlevel="' + level + '" class="plist-indentlevel-' + (level % 5) + '"></tr>');

	    if (readonlykey)
		key = idx++;

	    if (item.type == 'dictionary') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
		var children = generatePlistDOM(item.value, level + 1, false, options);
		rows = rows.concat(children);
	    }
	    else if (item.type == 'array') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
		var children = generatePlistDOM(item.value, level + 1, true, options);
		rows = rows.concat(children);
	    }
	    else if (item.type == 'bool') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else if (item.type == 'string') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else if (item.type == 'integer') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else if (item.type == 'float') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else if (item.type == 'data') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else if (item.type == 'date') {
		row.append(generatePlistDOMKey(key, readonlykey, level, options));
		row.append(generatePlistDOMType(item.type, level, options));
		row.append(generatePlistDOMValue(item.type, item.value, level, options));
		rows.push(row);
	    }
	    else
		console.log('Unknown item type ' + item.type);
	}

	return rows;
    }

    function generatePlistDOMKey(key, readonlykey, level, options)
    {
	var td = $('<td class="plist-key"></td>');

	td.append('<span class="plist-indent" style="width: ' + (level * 20) + 'px;">&nbsp;</span>');
	if (level > 0) {
	    var txt = $('<input type="text" class="plist-keyname" />');
	    txt.val(key);
	    if (readonlykey)
		$(txt).prop('readonly', true).data('inarray', '1');
	    if (level < options.protect)
		$(txt).prop('readonly', true);
	    td.append(txt);
	}
	else
	    td.append('<span class="plist-keyname">' + key + '</span>');

	return td;
    }

    function generatePlistDOMType(type, level, options)
    {
	var td = $('<td class="plist-type"></td>');
	var select = $('<select></select>');
	var option;

	$(select).append('<option value="dictionary">Dictionary</option>');
	$(select).append('<option value="array">Array</option>');
	if (level > 0) {
	    $(select).append('<option value="bool">Bool</option>');
	    $(select).append('<option value="string">String</option>');
	    $(select).append('<option value="date">Date</option>');
	    $(select).append('<option value="integer">Integer</option>');
	    $(select).append('<option value="float">Float</option>');
	    $(select).append('<option value="data">Data</option>');
	}
	$(select).val(type);
	if (level < options.protect)
	    $(select).prop('disabled', 'disabled');

	$(td).append(select);

	$(select).change(function () {
	    var tr = $(this).closest('tr');
	    var level = $(this).data('indentlevel');
	    var nx, obj;

	    // Erase the value of this row.
	    $(tr).children()[2].remove();
	    $(tr).append(generatePlistDOMValue($(this).val(), null, level, options));
	    // Erase all child rows, if any.
	    if ($(tr).next().length > 0) {
		for (obj = $(tr).next(); ; obj = nx) {
		    nx = $(obj).next();
		    if ($(nx).length == 0 || $(obj).data('indentlevel') <= $(tr).data('indentlevel'))
			break;
		    $(obj).remove();
		}
	    }
	});

	return td;
    }

    function generatePlistDOMValue(type, value, level, options)
    {
	var td = $('<td class="plist-value"></td>');
	var icons = $('<span class="plist-value-icons"></span>');

	if (type == 'dictionary') {
	    $(icons).append(plistExpandCollapseButton);
	    if (level + 1 >= options.protect)
		$(icons).append(plistAddButton(options));
	}
	else if (type == 'array') {
	    $(icons).append(plistExpandCollapseButton);
	    if (level + 1 >= options.protect)
		$(icons).append(plistAddButton(options));
	}
	else if (type == 'bool') {
	    var obj;
	    if (value == 1)
		obj = $('<input type="checkbox" checked />');
	    else
		obj = $('<input type="checkbox" />');
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}
	else if (type == 'string') {
	    var obj = $('<input type="text" data-regex="^.*$" />');
	    if (value)
		$(obj).val(value);
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}
	else if (type == 'integer') {
	    var obj = $('<input type="text" data-regex="^[0-9]+$" />');
	    $(obj).val((value ? value : "0"));
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}
	else if (type == 'float') {
	    var obj = $('<input type="text" data-regex="^[0-9]+(\.[0-9]+){0,1}$" />');
	    $(obj).val((value ? value : "0"));
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}
	else if (type == 'data') {
	    var obj = $('<input type="text" data-regex="^[a-zA-Z0-9+\\/=]$" />');
	    if (value)
		$(obj).val(value);
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}
	else if (type == 'date') {
	    var obj = $('<input type="text" data-regex="^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$" />');
	    if (value)
		$(obj).val(value);
	    if (level < options.protect)
		$(obj).attr('disabled', 'disabled');
	    $(td).append(obj);
	}

	if (level > 0 && level >= options.protect)
	    $(icons).append(plistDeleteButton());
	$(td).append(icons);

	return td;
    }

    function getUniqueKey(parent)
    {
	var key, tries = 0;

	if (parent) {
	    var level = $(parent).data('indentlevel');

	    key = 'New Key';
	    if ($(parent).next().length == 0)
		return key;

	    while (true) {
		for (obj = $(parent).next(); $(obj).length > 0; obj = $(obj).next()) {
		    if ($(obj).data('indentlevel') <= level)
			return key;
		    else if ($(obj).data('indentlevel') == (level + 1) && $(obj).find('span.plist-keyname').text() == key)
			break;
		}
		if ($(obj).length == 0)
		    return key;

		tries += 1;
		key = 'New Key ' + tries;
	    }
	}
	else {
	}

	return null;
    }

    function renumberPlistArray(parent)
    {
	var idx = 0, obj;
	var level = $(parent).data('indentlevel');


	for (obj = $(parent).next(); $(obj).length > 0; obj = $(obj).next()) {
	    if ($(obj).data('indentlevel') <= level)
		break;
	    if ($(obj).data('indentlevel') == (level + 1)) {
		$(obj).find('input.plist-keyname').val(idx);
		idx += 1;
	    }
	}
    }

    function processSaveLevel(rows, index, forlevel)
    {
	var text = '';

	for (; index < $(rows).length; index++) {
	    var row = $(rows).eq(index);
	    var type = $(row).find('select').val();
	    var key = $(row).find('td.plist-key input').val();
	    var val = $(row).find('td.plist-value input').val();
	    var level = $(row).data('indentlevel');
	    var tabs = Array(level + 1).join('\t');

	    if (level < forlevel) {
		index -= 1;
		break;
	    }

	    if ($(row).find('td.plist-key input').data('inarray') !== '1' && level > 0)
		key = tabs + '<key>' + key + '</key>\n';
	    else
		key = '';

	    if (type == 'dictionary') {
		text += key + tabs + '<dict>\n';
		var recurse = processSaveLevel(rows, index + 1, level + 1);
		index = recurse.index;
		text += recurse.text;
		text += tabs + '</dict>\n';
	    }
	    else if (type == 'array') {
		text += key + tabs + '<array>\n';
		var recurse = processSaveLevel(rows, index + 1, level + 1);
		index = recurse.index;
		text += recurse.text;
		text += tabs + '</array>\n';
	    }
	    else if (type == 'string') {
		text += key + tabs + '<string>' + escapeXml(val) + '</string>\n';
	    }
	    else if (type == 'bool') {
		text += key + tabs + ($(row).find('td.plist-value input').is(':checked') ? '<true/>' : '<false/>') + '\n';
	    }
	    else if (type == 'integer') {
		text += key + tabs + '<integer>' + val + '</integer>\n';
	    }
	    else if (type == 'float') {
		text += key + tabs + '<float>' + val + '</float>\n';
	    }
	    else if (type == 'data') {
		text += key + tabs + '<data>' + val + '</data>\n';
	    }
	    else if (type == 'date') {
		text += key + tabs + '<date>' + val + '</date>\n';
	    }
	}

	return { 'index': index, 'text': text };
    }

    function plistExpandCollapseButton()
    {
	var btn = $('<i class="fa fa-toggle-down"></i>');

	$(btn).click(function () {
	    var tr = $(this).closest('tr');
	    var nx, obj;
	    var show = $(this).hasClass('fa-toggle-right');

	    if ($(tr).next().length > 0) {
		for (obj = $(tr).next(); $(obj).length > 0; obj = nx) {
		    nx = $(obj).next();
		    if ($(obj).data('indentlevel') <= $(tr).data('indentlevel'))
			break;

		    if (show) {
			$(obj).show();
			$(obj).find('i.fa-toggle-right').removeClass('fa-expand').addClass('icon-toggle-down');
		    }
		    else
			$(obj).hide();
		}
	    }

	    if (show)
		$(this).removeClass('fa-toggle-right').addClass('fa-toggle-down');
	    else
		$(this).removeClass('fa-toggle-down').addClass('fa-toggle-right');
	});

	return btn;
    }

    function plistAddButton(options)
    {
	var btn = $('<i class="fa fa-plus"></i>');

	$(btn).click(function () {
	    var tr = $(this).closest('tr');
	    var type = $(tr).find('select').val();
	    var nx, obj, lst;
	    var level = ($(tr).data('indentlevel') + 1);
	    var newrow = $('<tr data-indentlevel="' + level + '" class="plist-indentlevel-' + (level % 5) + '"></tr>');
	    var key = (type == 'dictionary' ? getUniqueKey($(tr)) : '-1');

	    newrow.append(generatePlistDOMKey(key, (type == 'array'), level, options));
	    newrow.append(generatePlistDOMType('string', level, options));
	    newrow.append(generatePlistDOMValue('string', null, level, options));

	    if ($(tr).next().length > 0) {
		for (lst = tr, obj = $(tr).next(); ; lst = obj, obj = nx) {
		    nx = $(obj).next();
		    if ($(nx).length == 0) {
			$(obj).after(newrow);
			break;
		    }
		    if ($(obj).data('indentlevel') <= $(tr).data('indentlevel')) {
			$(lst).after(newrow);
			break;
		    }
		}
	    }
	    else
		$(tr).after(newrow);

	    if (type == 'array')
		renumberPlistArray($(tr));
	});

	return btn;
    }

    function plistDeleteButton()
    {
	var btn = $('<i class="fa fa-times"></i>');

	$(btn).click(function () {
	    var tr = $(this).closest('tr');
	    var nx, obj;

	    if ($(tr).next().length > 0) {
		for (obj = $(tr).next(); $(obj).length > 0; obj = nx) {
		    nx = $(obj).next();
		    if ($(obj).data('indentlevel') <= $(tr).data('indentlevel'))
			break;
		    $(obj).remove();
		}
	    }
	    $(tr).remove();
	});

	return btn;
    }

    function parsePropertyListNode(node)
    {
	if ($(node).get(0).nodeName.toLowerCase() == 'dict') {
	    var result = [ ];

	    for (var idx = 0; (idx + 1) < $(node).children().length; idx += 2) {
		var key = $(node).children().eq(idx).text();
		var value = parsePropertyListNode($(node).children().eq(idx + 1));
		if (value != null) {
		    value['key'] = key;
		    result.push(value);
		}
		else
		    console.log('Got null for key ' + key + ', ' + $(node).children().eq(idx + 1).get(0).nodeName);
	    }

	    return { 'type': 'dictionary', 'value': result };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'array') {
	    var result = [ ];

	    for (var idx = 0; idx < $(node).children().length; idx++) {
		var value = parsePropertyListNode($(node).children().eq(idx));
		if (value != null)
		    result.push(value);
	    }

	    return { 'type': 'array', 'value': result };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'string') {
	    return { 'type': 'string', 'value': $(node).text() };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'integer') {
	    return { 'type': 'integer', 'value': parseInt($(node).text()) };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'real') {
	    return { 'type': 'float', 'value': parseFloat($(node).text()) };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'true') {
	    return { 'type': 'bool', 'value': 1 };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'false') {
	    return { 'type': 'bool', 'value': 0 };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'data') {
	    return { 'type': 'data', 'value': $(node).text().replace(/[^a-zA-Z0-9+\/=]/g, '') };
	}
	else if (node.get(0).nodeName.toLowerCase() == 'date') {
	    return { 'type': 'date', 'value': $(node).text() };
	}

	console.log('unknown node: ' + $(node).get(0).nodeName);

	return null;
    }

})( jQuery );

