import React from "react";
import PropTypes from "prop-types";


class Comment extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            text: "",
            comments: [],
            commentsUrl: "", 
        }
    }


    componentDidMount() {
        // This line automatically assigns this.props.url to the const variable url
        const { commentsList, url } = this.props;
        // Call REST API to get the post's information
        this.setState({
            comments: commentsList,
            commentsUrl: url
        });
    }


    handleChange(event) {
        this.setState({ text: event.target.value });
    }


    handleSubmit(commentsUrl, event) {
        event.preventDefault();
        const{ text } = this.state;
        fetch(commentsUrl, {
            credentials: "same-origin", 
            method: "POST", 
            headers: {'Content-Type': 'application/json'}, 
            body: JSON.stringify(text)
        })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState(prevState => ({
                    text: "",
                    comments: prevState.comments.concat(data)
                }));
            })
            .catch((error) => console.log(error));
    }

    handleDeleteClick(url, id) {
        const { comments } = this.state;
        fetch(url, { credentials: "same-origin", method: "DELETE" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then(() => {
                this.setState({
                    comments: comments.filter(c => c.commentid !== id)
                });
            })
            .catch((error) => console.log(error));
    }

    render() {
        const {text, comments, commentsUrl} = this.state
        return (
            comments.map((comment) => (
                <div>
                    <div>
                        <a href="/users/{{comment.owner}}/">
                            {comment.owner}
                        </a>
                        {comment.text}
                    </div>
                    <div>
                        {comment.lognameOwnsThis
                        ? 
                        <button
                            type="button"
                            className="delete-comment-button"
                            onClick={this.handleDeleteClick(comment.url, comment.commentid)}
                        >
                            Delete comment
                        </button>
                        : 
                        null}
                    </div>
                    <div>
                        <form
                            className="comment-form"
                            onSubmit={(e) => {this.handleSubmit(e, commentsUrl)}}
                        >
                            <input
                                type="text"
                                value={text}
                                onChange={this.handleChange}
                            />
                        </form>
                    </div>
                </div>
            ))
        );
    }
}
Comment.propTypes = {
    url: PropTypes.string.isRequired,
    commentsList: PropTypes.arrayOf(Object).isRequired,
};
export default Comment;
