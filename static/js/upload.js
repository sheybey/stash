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

	function upload(file) {
		var form, xhr, progress, cancel;

		function error() {
			textwithbrowse(droptarget, "Failed. Drop a file or", "to try again");
		}

		if (running) {
			return;
		}
		running = true;

		form = new FormData();
		xhr = new XMLHttpRequest();
		progress = document.createElement("progress");
		cancel = document.createElement("button");

		form.append("file", file);
		cancel.textContent = "Cancel";
		cancel.addEventListener("click", function () {
			xhr.abort();
		});
		progress.max = file.size;
		droptarget.textContent = "";
		droptarget.appendChild(progress);
		droptarget.appendChild(cancel);

		xhr.addEventListener("progress", function (event) {
			progress.value = event.loaded;
		});
		xhr.addEventListener("load", function () {
			textwithbrowse(droptarget, "Finished. Drop or", "to upload another file");
		});
		xhr.addEventListener("abort", error);
		xhr.addEventListener("error", error);
		xhr.addEventListener("loadend", function () {
			running = false;
		});
		xhr.open("POST", "upload");
		xhr.send(form);
	}

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
	input.addEventListener("change", function () {
		if (!running && input.files[0]) {
			upload(input.files[0]);
		}
	});
});