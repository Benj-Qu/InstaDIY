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

  handleClick() {
    // const hasLiked = this.state.hasLiked;
    const { url, hasLiked, numLikes } = this.props;
    this.setState({
      has_liked: hasLiked,
      num_likes: numLikes
    })

    if (hasLiked === false)
    {
      this.state.has_liked = true;
      this.state.num_likes += 1;
      
      fetch(url, { credentials: "same-origin", method: "POST" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));

    }
    if (hasLiked === true)
    {
      this.state.has_liked = false;
      this.state.num_likes -= 1;

      fetch(url, { credentials: "same-origin", method: "DELETE" })
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
    const { hasLiked, numLikes } = this.props;
    // Render post image and post owner
    return (
      <div>
        <div>
          <button 
            type='button'
            className="like-unlike-button" 
            onClick={() => this.handleClick()}
          >
            {hasLiked? "unlike" : ""}
          </button>
        </div>
        <div>
          {numLikes}
          {" "}
          {numLikes === 1? "like" : "likes"}
        </div>
      </div>
    );
  }
}

Like.propTypes = {
  url: PropTypes.string.isRequired,
  hasLiked: PropTypes.bool.isRequired,
  numLikes: PropTypes.number.isRequired
};

export default Like;
