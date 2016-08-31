HTMLCollection.prototype.forEach = function (callback) {
	for (var i = 0; i < this.length; i += 1) {
		callback.call(this, this[i], i, this);
	}
};

document.addEventListener("DOMContentLoaded", function () { 
	document.getElementsByClassName("error").forEach(function (element) {
		closebutton = document.createElement("a");
		closebutton.textContent = "\u00d7";
		closebutton.href = "#";
		closebutton.addEventListener("click", function (event) {
			event.preventDefault();
			event.stopPropagation();
			element.parentNode.removeChild(element);
		});
		element.appendChild(closebutton);
	});
});