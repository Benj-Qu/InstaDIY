import React from "react";
// import PropTypes from "prop-types";

class Like extends React.Component {
  /* Display image and post owner of a single post
   */
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {
      hasLiked: false,
      numLikes: 0
    };
  }

  handleClick() {
    const { hasLiked } = this.state;

    if (hasLiked === false)
    {
      this.state.hasLiked = true;
      this.state.numLikes += 1;
    }
    else
    {
      this.state.hasLiked = false;
      this.state.numLikes -= 1;
    }
    
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { hasLiked, numLikes } = this.state;
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

export default Like;
