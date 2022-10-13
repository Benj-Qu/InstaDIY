import React from "react";
import PropTypes from "prop-types";
class Like extends React.Component {
  /* Display image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {};
  }

  handleClick() {
    // const hasLiked = this.state.hasLiked;
    const { hasLiked } = this.props;
    if (hasLiked === false)
    {
      this.props.hasLiked = true;
      this.props.numLikes += 1;
    }
    else
    {
      this.props.hasLiked = false;
      this.props.numLikes -= 1;
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
