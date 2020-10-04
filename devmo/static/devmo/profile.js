document.addEventListener('DOMContentLoaded', function() {
	fetch(`${window.location.pathname}/info`)
        .then(response => response.json())
        .then(data => {
            if (data.session_user == null) {
                console.log('Not signed in')
                document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/plus.png");
            } else if (data.session_user.username == data.info.username) {
                console.log('Your profile')
            } else {
                if (data.isFollow == 'yes') {
                    document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/checkmark.png");
                } else {
                    document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/plus.png");
                }
            }
            define_user(data)
        })
})

function define_user(info) {
        document.querySelector('.username').innerHTML = info.info.username
        document.querySelector('.followers_count').innerHTML = info.info.followers
        if (info.session_user == null) {
            document.querySelector('.follow_button').onclick = function fun() {
                alert("You need to sign in.");
            }
        } else if (info.session_user.username == info.info.username) {
                
        } else {
            document.querySelector('.follow_button').onclick = function fun() {
                follow(info.info.username);
            }
        }
        document.querySelector('.following_count').innerHTML = info.following
        document.querySelector('.user_pic').setAttribute("src", `${info.user.user_pic}`)
    }

function follow(username) {
        fetch(`/follow/${username}`, {
            method: 'POST',
            body: JSON.stringify({
        })
})
        .then(response => response.json())
        .then(data => {
            document.querySelector('.followers_count').innerHTML = data.info.followers;
            document.querySelector('.following_count').innerHTML = data.following
            if (data.isFollow == 'yes') {
                document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/checkmark.png");
            } else {
                document.querySelector('.plus_icon').setAttribute("src", "/static/devmo/images/plus.png");
            }
            
        })
    }