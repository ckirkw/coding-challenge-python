window.Blog = window.Blog || {};

(() => {
    
    /**
     * Retrieves article comments from the database and renders them in the DOM
     */
    Blog.loadComments = articleId => {
        $.ajax(`/posts/${articleId}/comments`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: response => {
                Blog.checkSubmitEnabled();
                const results = JSON.parse(response);
                if (results.length == 0) {
                    $('#no_comments').css({'display': 'inline'});
                    return;
                }

                results.forEach(result => {
                    addCommentToDOM(result.fields);
                });
            }
        });
    };
    
    /**
     * Saves a comment to the database
     */
    Blog.submitComment = articleId => {
        const comment = $('#comment').val().trim();
        if (comment == '')
            return;

        const data = `comment=${encodeURIComponent(comment)}`;
        $.ajax(`/posts/${articleId}/comments`, {
            method: 'POST',
            data: data,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: response => {
                const result = JSON.parse(response)[0];
                addCommentToDOM(result.fields);
                $('#comment').val('');
            }
        });
    };

    /**
     * Enables or disables the "Submit" button for the comments section
     * based on whether the comment is empty or not
     */
    Blog.checkSubmitEnabled = () => {
        const comment = $('#comment').val().trim();
        if (comment.trim() == '')
            $('#comment_submit').prop('disabled', true);
        else
            $('#comment_submit').removeAttr('disabled');
    };

    const addCommentToDOM = comment => {
        const fullName = (comment.user.first_name + ' ' + comment.user.last_name).trim();

        const articleTemplate = 
        `<article class="media">
            <figure class="media-left">
            <p class="image is-64x64">
                <img src="https://bulma.io/images/placeholders/128x128.png">
            </p>
            </figure>
            <div class="media-content">
            <div class="content">
                <p>
                <strong>${fullName}</strong> <small>@${comment.user.username}</small>
                <br>
                ${comment.comment}
                </p>
            </div>
            <nav class="level is-mobile">
                <div class="level-left">
                <a class="level-item">
                    <span class="icon is-small"><i class="fa fa-thumbs-up"></i></span>
                </a>(10)&nbsp;·&nbsp;<a class="level-item link">Reply</a>
                </div>
            </nav>
            </div>
        </article>`;

        $('#comment_list').append($(articleTemplate));
    };

    const getCookie = name => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

})();
