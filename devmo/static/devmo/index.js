document.addEventListener('DOMContentLoaded', function() {

    // Select all buttons
    document.querySelectorAll('.each_category').forEach(button => {

        // When a button is clicked, show posts by the category
        button.onclick = function() {
            showCategory(this.dataset.category);
        }
    })
});

function showCategory(category) {

	var list = document.querySelectorAll('.each_project');
	var elArr = Array.from(list);
	elArr.forEach(element=> {
		if (element.dataset.category == category || category == "all" ) {
			element.style.display = 'block';
		} else {
			element.style.display = 'none';
		}
	});
}