document.addEventListener("DOMContentLoaded", function () {
	"use strict";
	var droptarget = document.getElementById("droptarget"),
		input = document.getElementById("file"),
		running = false;

	function textwithbrowse(elem, before, after) {
		var browse = document.createElement("a");
		browse.textContent = "browse";
		browse.href = "#";
		browse.addEventListener("click", function (event) {
			event.preventDefault();
			event.stopPropagation();
			input.click();
		});

		elem.textContent = before + " ";
		elem.appendChild(browse);
		elem.appendChild(document.createTextNode(" " + after));
	}

	input.parentNode.parentNode.classList.add("hidden");
	droptarget.classList.remove("hidden");
	textwithbrowse(droptarget, "Drop a file here or", "to upload it");

	droptarget.addEventListener("dragover", function (event) {
		event.stopPropagation();
		event.preventDefault();
		if (running) {
			event.dataTransfer.dropEffect = "none";
		} else {
			event.dataTransfer.dropEffect = "copy";
			droptarget.classList.add("dragover");
		}
	});
	droptarget.addEventListener("dragleave", function () {
		droptarget.classList.remove("dragover");
	});
	droptarget.addEventListener("drop", function (event) {
		event.stopPropagation();
		event.preventDefault();
		if (running) {
			return;
		}
		droptarget.classList.remove("dragover");
		if (event.dataTransfer.files.length > 0) {
			upload(event.dataTransfer.files[0]);
		}
	});

});