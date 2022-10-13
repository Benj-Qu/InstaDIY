import React from "react";
import PropTypes from "prop-types";

class Like extends React.Component {
  /* Display image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      has_liked: false,
      num_likes: 0
    };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { likes } = this.props;
    // Call REST API to get the post's information
    this.setState({
      has_liked: likes.hasLiked,
      num_likes: likes.numLikes
    })
  }

  handleClick() {
    // const hasLiked = this.state.hasLiked;
    const { likes } = this.props;
    this.setState({
      has_liked: likes.hasLiked,
      num_likes: likes.numLikes
    })

    if (likes.hasLiked === false) {
      this.state.has_liked = true;
      this.state.num_likes += 1;

      fetch(likes.url, { credentials: "same-origin", method: "POST" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .catch((error) => console.log(error));

    }
    if (likes.hasLiked === true) {
      this.state.has_liked = false;
      this.state.num_likes -= 1;

      fetch(likes.url, { credentials: "same-origin", method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .catch((error) => console.log(error));
    }
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { likes } = this.props;
    // Render post image and post owner
    return (
      <div>
        <div>
          <button
            type='button'
            className="like-unlike-button"
            onClick={() => this.handleClick()}
          >
            {likes.hasLiked ? "unlike" : ""}
          </button>
        </div>
        <div>
          {likes.numLikes}
          {" "}
          {likes.numLikes === 1 ? "like" : "likes"}
        </div>
      </div>
    );
  }
}

Like.propTypes = {
  likes: PropTypes.objectOf(PropTypes.bool, PropTypes.number, PropTypes.string).isRequired,
};

export default Like;
