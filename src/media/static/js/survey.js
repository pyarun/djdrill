$(document).ready(function() {
	//enable collapse and expand on list
	$(".demo").collapse({
		query : 'div h2'
	});

	//to display form for adding new list
	$("button#add_new_list").click(function() {
		$("div#add-list-form").show();
	});

	//to diplay input for new entry in list
	$("button#add_new_entry").click(function() {
		var newentryinput = $("<input>").attr({
			"name" : "entry",
			"type" : "text"
		});
		var newli = $("<li>").append(newentryinput);
		$("div#add-entries ul").append(newli);
	})

	$("button.add_entry_button").click(function() {
		var id = $(this).attr("id");
		id = id.split("-")[1];
		var newentryinput = $("<input>").attr({
			"name" : "entry",
			"type" : "text",
			"id" : "entry-" + id + "-0"
		});
		var newli = $("<li>").append(newentryinput);
		$(this).next("button").removeAttr("disabled");
		var entriesul = $(this).nextAll("form").first().find("ul");
		entriesul.append(newli);
	});

	$(".save_entry_button").click(function() {
		var form = $(this).nextAll("form").first();
		form.submit();
	});

	//deletes the entry from List
	$(".remove-entry").live("click", function() {
		var elem = $(this);
		var tagid = $(this).attr("id");
		var listid = tagid.split("-")[1];
		var elemid = tagid.split("-")[2];
		var data = {
			"listid" : listid,
			"elemid" : elemid,
			"csrfmiddlewaretoken" : $.cookie("csrftoken")
		};
		var url = "{% url remove_elem %}";
		$.post(url, data, function(data, status, xhr) {
			if (status == "success" && data == "true") {
				elem.parent().remove();
				var ul = elem.parentsUntil("ul").last().parent()debugger;
				$.each(ul.children(), function(index, item) { debugger;

				})
			}

		})
	});

	//delete a list
	$(".delete-list").click(function() {
		var elem = $(this);
		var eltagid = elem.attr("id");
		var listid = eltagid.split("-")[2];
		var url = "{% url delete_list %}";
		var data = {
			"listid" : listid,
			"csrfmiddlewaretoken" : $.cookie("csrftoken")
		};
		$.post(url, data, function(data, status, xhr) {
			if (status == "success" && data == "true") {
				ab = elem.parentsUntil(".demo").last().parent().remove();
			}

		})
	});

}); 