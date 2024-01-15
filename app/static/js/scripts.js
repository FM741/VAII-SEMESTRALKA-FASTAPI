function scrollNavbar() {
    if (window.scrollY >= navbarPos) {
        navbar.classList.add("sticky");
    } else {
        navbar.classList.remove("sticky", "");
    }
}

const dropdownBtn = document.querySelector(".navbar-collapse");
const content = document.querySelector(".navbar-collapse-content");

document.addEventListener('click', (evt) => {
    if (!content.contains(evt.target) && !dropdownBtn.contains(evt.target)) {
        content.classList.remove('navbar-collapse-content--opened');
    }
});

dropdownBtn.addEventListener('click', (_evt) => {
    content.classList.toggle('navbar-collapse-content--opened');
});

// Ajax calls
let url = window.location.href.split("/")
const submitForum = () => {
    console.log('request_body_param pushed')
    let forum = {
        "name": $("#forum_name").val(),
    };
    $.ajax({
        url: "/crud/forum/add",
        type: "POST",
        data: JSON.stringify(forum),
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log("success", data);
            window.location = "/";
        },
        error: function (xhr, error) {
            alert("STATUS: " + xhr.status + "\nCannot create -" + JSON.parse(xhr.responseText).detail);
        }
    });
}

const editForum = (forum_id) => {
    let forum = {
        "name": $("#forum_name").val()
    };
    console.log(forum)
    $.ajax({
        url: "/crud/forum/" + forum_id,
        type: "PATCH",
        data: JSON.stringify(forum),
        dataType: "json",
        contentType: "application/json",
        success: function () {
            window.location = document.referrer
        },
        error: function (xhr, error) {
            alert("STATUS: " + xhr.status + "\n" + JSON.parse(xhr.responseText).detail);
        }
    });
}
const submitTopic = () => {
    console.log('request_body_param pushed')
    let topic = {
        "name": $("#topic_name").val(),
        "forum_id": url[4],
    };
    $.ajax({
        url: "/crud/topic/add",
        type: "POST",
        data: JSON.stringify(topic),
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log("success", data);
            let post = {
                "header": $("#post_header").val(),
                "body": $("#post_body").val(),
                "topic_id": data.id
            };
            addPost(post)
        },
    });
}

const editTopic = (topic_id) => {
    let topic = {
        "name": $("#topic_name").val(),
        "forum_id": $("#select_forum").val()
    };
    console.log(topic)
    $.ajax({
        url: "/crud/topic/" + topic_id,
        type: "PATCH",
        data: JSON.stringify(topic),
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            window.location = "/forum/" + data.forum_id;
        },
    });
}

const submitPost = () => {
    console.log('request_body_param pushed')
    let post = {
        "header": $("#header").val(),
        "body": $("#text-area").val(),
        "topic_id": url[4]
    };
    addPost(post)
}

const deleteForum = (forum_id) => {
    if (dangerousCheck()) {
        return;
    }

    $.ajax({
        url: "/crud/forum/" + forum_id,
        type: "DELETE",
        dataType: "json",
        contentType: "application/json",
        success: function () {
            window.location.reload();
        },
    });
}

const deleteTopic = (topic_id) => {
    if (dangerousCheck()) {
        return;
    }

    $.ajax({
        url: "/crud/topic/" + topic_id,
        type: "DELETE",
        dataType: "json",
        contentType: "application/json",
        success: function () {
            console.log("removed");
            window.location.reload();
        },
    });
}


const deletePost = () => {
    if (dangerousCheck()) {
        return;
    }
    let post_id = $("#post_id_hidden").val();
    $.ajax({
        url: "/crud/post/" + post_id,
        type: "DELETE",
        dataType: "json",
        contentType: "application/json",
        success: function () {
            console.log("removed");
            window.location.reload();
        },
    });
}

const editPost = (post_id) => {
    let post = {
        "header": $("#post_header").val(),
        "body": $("#post_body").val()
    }
    $.ajax({
        url: "/crud/post/" + post_id,
        type: "PATCH",
        data: JSON.stringify(post),
        dataType: "json",
        contentType: "application/json",
        success: function () {
            window.location = document.referrer;
        },
    });
}


const addPost = (post) => {
    console.log("sending", post)
    $.ajax({
        url: "/crud/post/add",
        type: "POST",
        data: JSON.stringify(post),
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log("success", data);
            window.location = "/topic/" + data.topic_id;
        }
    });
}

const submitUser = () => {
    console.log('request_body_param pushed')
    let user = {
        "username": $("#username").val(),
        "password": $("#password").val(),
        "gender": $('input[name="gender"]:checked').val(),
        "date_of_creation": new Date(),
    };
    $.ajax({
        url: "/crud/user/add",
        type: "POST",
        data: JSON.stringify(user),
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            console.log("success", data);
            window.location = "/";
        },
        error: function (xhr, error) {
            alert("STATUS: " + xhr.status + "\nCannot create -" + JSON.parse(xhr.responseText).detail);
        }
    });
}


const loginUser = () => {
    console.log('request_body_param pushed')
    let user = {
        "username": $("#username").val(),
        "password": $("#password").val(),
    };
    $.ajax({
        url: "/token",
        type: "POST",
        data: $.param(user),
        dataType: "json",
        contentType: "application/x-www-form-urlencoded",
        xhrFields: {withCredentials: true},
        crossDomain: true,
        success: function (data) {
            console.log("success", data);
            window.location = "/";
        },
        error: function (xhr, error) {
            let message = JSON.parse(xhr.responseText).detail;
            $("#error").html(message);
        }
    });
}

const dangerousCheck = () => {
    return confirm("Are you sure? This might delete all children!") === false;
}