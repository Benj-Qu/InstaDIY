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
    // console.log(likes);
    // console.log(likes.lognameLikesThis);
    // console.log(likes.numLikes);
    // Call REST API to get the post's information
    this.setState({
      has_liked: likes.hasLiked,
      num_likes: likes.numLikes
    })
  }



  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { likes } = this.props;
    // Render post image and post owner
    return (
      
    );
  }
}

Like.propTypes = {
  // lognameLikesThis: PropTypes.bool.isRequired,
  // numLikes: PropTypes.number.isRequired,
  // url: PropTypes.string.isRequired
  likes: PropTypes.objectOf(
    PropTypes.bool.isRequired,
    PropTypes.number.isRequired,
    PropTypes.string.isRequired,
  ).isRequired,
};

export default Like;
