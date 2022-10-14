import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Comment from "./comment";

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: [],
      commentsUrl: "",
      created: "",
      imgUrl: "",
      lognameLikesThis: false,
      numLikes: 0,
      likesUrl: "",
      owner: "",
      ownerImgUrl: "",
      ownerShowUrl: "",
      postShowUrl: "",
      postid: 0
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
          lognameLikesThis: data.likes.lognameLikesThis,
          numLikes: data.likes.numLikes,
          likesUrl: data.likes.url,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
          postid: data.postid,
        });
      })
      .catch((error) => console.log(error));
  }

  likeClick() {
    const { lognameLikesThis, likesUrl, postid } = this.state

    if (lognameLikesThis === false) {
      const likePostUrl = `/api/v1/likes/?postid=${postid}`
      fetch(likePostUrl, { credentials: "same-origin", method: "POST" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState(prevState => ({
            lognameLikesThis: true,
            numLikes: prevState.numLikes + 1,
            likesUrl: data.url
          }))
        })
        .catch((error) => console.log(error));
    }
    else {
      fetch(likesUrl, { credentials: "same-origin", method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .catch((error) => console.log(error));
      this.setState(prevState => ({
        lognameLikesThis: false,
        numLikes: prevState.numLikes - 1,
        likesUrl: null
      }))
    }
  }

  render() {
    const { comments, commentsUrl, created, imgUrl,
      lognameLikesThis, numLikes, owner, ownerImgUrl, ownerShowUrl,
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
              onClick={() => this.likeClick()}
            >
              {lognameLikesThis ? "unlike" : "like"}
            </button>
          </div>
          <div>
            {numLikes}
            {numLikes === 1 ? " like" : " likes"}
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
