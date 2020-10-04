document.addEventListener('DOMContentLoaded', function() {
	
})

function like(id) {
	console.log("Like was clicked!", id)
	fetch(`/like/${id}`, {
  		method: 'POST'
	})
		.then(response => response.json())
	    .then(data => {
	    	console.log("New count of likes is", data.info.likes);
	    	if (data.like == 'yes') {
	    		document.querySelector('.fa-heart').setAttribute("class", "fas fa-heart");
	    	} else {
	    		document.querySelector('.fa-heart').setAttribute("class", "far fa-heart");
	    	}
		})

}

function bookmark(id) {
	console.log("Bookmarked id:", id)
	fetch(`/favorites/${id}`, {
  		method: 'POST'
	})
		.then(response => response.json())
	    .then(data => {
	    	console.log(`isBookmarked? : ${data.isBookmarked}`)
	    	if (data.isBookmarked == 'yes') {
	    		document.querySelector('#fa-bookmark').setAttribute("class", "fas fa-bookmark");
	    	} else {
	    		document.querySelector('#fa-bookmark').setAttribute("class", "far fa-bookmark");
	    	}
		})
}

function follow(username) {
	console.log(username)
        fetch(`/follow/${username}`, {
            method: 'POST',
            body: JSON.stringify({
        })
})		
        .then(response => response.json())
	    .then(data => {
	    	console.log(data.isFollow)
	    	if (data.isFollow == 'yes') {
	    		document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/checkmark.png");
	    	} else {
	    		document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/plus.png");
	    	}
	    })
    }

function alert_message() {
	alert('You need to sign in.');
}