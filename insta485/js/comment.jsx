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
        const { commentsListl, url } = this.props;
        // Call REST API to get the post's information
        this.setState({
            comments: commentsList,
            commentsUrl: url
        });
    }


    handleChange(event) {
        this.setState({ text: event.target.value });
    }


    handleSubmit(event) {
        event.preventDefault();
    }

    handleDeleteClick(url, id) {
        const { comments } = this.state;
        fetch(url, { credentials: "same-origin", method: "DELETE" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState({
                    comments: comments.filter(c => c.commentid !== id)
                });
            })
            .catch((error) => console.log(error));
    }

    render() {

    }
}
Comment.propTypes = {
    url: PropTypes.string.isRequired,
};
export default Comment;
