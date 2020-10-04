document.addEventListener('DOMContentLoaded', function() {
	console.log(document.querySelector('#category').value)

})

function newpost() {
	console.log('YES')
	fetch('/newpost', {
  	method: 'POST',
  	body: JSON.stringify({
  		title: document.querySelector('#title').value,
      	content: document.querySelector('#content').value,
      	image: document.querySelector('#image').value,
      	category: document.querySelector('#category').value
  		})
	})
	document.querySelector('#title').value = '';
	document.querySelector('#content').value = '';
	document.querySelector('#image').value = '';
	document.querySelector('#category').value = '';
	document.querySelector('.succsess_text').style.display = 'block';
}