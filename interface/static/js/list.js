// Django Get Cookie Suggested Function
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var KeyStore = {
	openRow: null,
	default_name: "New Row",
	default_value: "",
	selectOpenRow: function() {
		if(KeyStore.openRow==-1) {
			return $("tr.keypair.new");	
		} else {
			return $("tr.keypair[data-kpid='" + KeyStore.openRow + "']");
		}
	},
	keyHandler: function(e) {
	    if(e.which == 13) {
	        KeyStore.closeEditor();
	    }
	},
	editorHandler: function(event) {
		event.stopPropagation();

		var kpid = $(this).attr('data-kpid');

		// If no editor open, open row for editing
		if(KeyStore.openRow==null) {
			KeyStore.openEditor(this);

		// Row is open already, if different row requests, close current
		// then open new on callback
		} else {
			if(KeyStore.openRow!=-1 && KeyStore.openRow!=kpid) {
				KeyStore.closeEditor({ "fn": KeyStore.openEditor, "args": this });
			}
		}
	},
	openEditor: function(keypair) {

		var kpid = $(keypair).attr('data-kpid');

		if(typeof kpid === "undefined") {
			kpid = -1
		}

		KeyStore.openRow = kpid;

		$(keypair).addClass('open');

		var key_name = $(keypair).find('.name');
		var key_value = $(keypair).find('.value');

		var key_name_value = key_name.text();
		var key_value_value = key_value.text();

		key_name.text('');
		key_name.append($('<input/>', { "value": key_name_value, "name": "key_name" }));

		key_value.text('');
		key_value.append($('<input/>', { "value": key_value_value, "name": "key_value" }));
	},
	closeEditor: function(callback) {

		var open = KeyStore.selectOpenRow();

		open.removeClass('open');

		KeyStore.postEdited(open);

		var key_name = $(open).find('.name');
		key_name.text(key_name.find('input').val());

		var key_value = $(open).find('.value');
		key_value.text(key_value.find('input').val());

		KeyStore.openRow = null;

		if(typeof callback !== "undefined") {
			callback.fn(callback.args);
		}

	},
	postSuccess: function(data) {

		if($("tr.keypair[data-kpid='" + data.kpid + "']").length==0) {
			$('tr.keypair.new').attr('data-kpid', data.kpid).removeClass('new');

			$('table.keypair_list').append(
				$('<tr/>', { "class": "keypair new" })
				.append($('<td/>', { "class": "name", "text": KeyStore.default_name }))
				.append($('<td/>', { "class": "value", "text": KeyStore.default_value }))
			);

			KeyStore.bindRows();
		}
	},
	postEdited: function(keypair) {

		$.ajax({
			url: "/api/keypair/",
			type: "POST",
			data: {
				"kpid": keypair.attr('data-kpid'),
				"key_name": keypair.find('.name input').val(),
				"key_value": keypair.find('.value input').val(),
			},
			success: KeyStore.postSuccess,
			error: function(data) {
				// Handle failure to save
			},
			beforeSend: function(xhr, settings) {
	            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    	}
	  	});
	},
	blur: function() {
		if(KeyStore.openRow!=null) {
			KeyStore.closeEditor();
		}
	},
	bindRows: function() {
		$('tr.keypair').unbind("click");
		$('tr.keypair').bind("click", KeyStore.editorHandler);
	},
	remove: function(e) {
		e.stopPropagation();

		var kpid = $(this).attr('data-kpid');
		console.log('delete', kpid);
		$.ajax({
			url: "/api/keypair/",
			type: "DELETE",
			data: {
				"kpid": kpid,
			},
			success: KeyStore.postSuccess,
			error: function(data) {
				// Handle failure to save
			},
			beforeSend: function(xhr, settings) {
	            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	    	}
	  	});
	},
	initialize: function() {
		$(document).keypress(KeyStore.keyHandler);
		KeyStore.bindRows();
		$('html').bind("click", KeyStore.blur);
		$('td.remove').bind("click", KeyStore.remove);
	}
}

$(document).ready(KeyStore.initialize);