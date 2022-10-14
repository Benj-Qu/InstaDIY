import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Like from "./like";
import Comment from "./comment";

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: [],
      commentsUrl: "",
      created: "",
      imgUrl: "",
      likes: {},
      owner: "",
      ownerImgUrl: "",
      ownerShowUrl: "",
      postShowUrl: "",
    };
  }

  componentDidMount() {
    const { url } = this.props;
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
          commentsUrl: data.comments_url,
          created: data.created,
          imgUrl: data.imgUrl,
          likes: data.likes,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
        });
      })
      .catch((error) => console.log(error));
  }

  handleClick() {
    // const hasLiked = this.state.hasLiked;
    const { likes } = this.state

    if (likes.hasLiked === false) {
      fetch(likes.url, { credentials: "same-origin", method: "POST" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .catch((error) => console.log(error));

      this.setState(prevState => ({
        likes: {
          lognamesLikesThis: true,
          numLikes: prevState.likes.nummLikes + 1,
          url: ""
        }
      }))



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
    const { comments, commentsUrl, created, imgUrl,
      likes, owner, ownerImgUrl, ownerShowUrl,
      postShowUrl } = this.state;
    const { timestamp } = moment(created).fromNow();
    return (
      <div>
        <div>
          <a href={ownerShowUrl}>
            <img src={ownerImgUrl} alt={ownerImgUrl} />
            <div> {owner} </div>
          </a>
        </div>
        <div>
          <a href={postShowUrl}>{timestamp}</a>
        </div>
        <div>
          <img src={imgUrl} alt={imgUrl} />
        </div>
        <div>
          <div>
            <button
              type='button'
              className="like-unlike-button"
              onClick={() => this.handleClick()}
            >
              {likes.hasLiked ? "unlike" : "like"}
            </button>
          </div>
          <div>
            {likes.numLikes}
            {likes.numLikes === 1 ? " like" : " likes"}
          </div>
        </div>
        <Comment comments={comments} commentsUrl={commentsUrl} />
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
