HTMLCollection.prototype.forEach = function (callback) {
	"use strict";
	for (var i = 0; i < this.length; i += 1) {
		callback.call(this, this[i], i, this);
	}
};

document.addEventListener("DOMContentLoaded", function () {
	"use strict";
	document.getElementsByClassName("error").forEach(function (error) {
		var closebutton = document.createElement("a");
		closebutton.textContent = "\u00d7";
		closebutton.href = "#";
		closebutton.addEventListener("click", function (event) {
			event.preventDefault();
			event.stopPropagation();
			error.parentNode.removeChild(error);
		});
		error.appendChild(closebutton);
	});
});