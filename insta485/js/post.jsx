import React from "react";
import PropTypes from "prop-types";
import moment from "moment";

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
      postid: 0,
      newComment: "",
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
    const { comments } = this.state;
    console.log(comments);
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

  handleChange(event) {
    this.setState({ newComment: event.target.value });
  }


  handleSubmit(commentsUrl, event) {
    event.preventDefault();
    const { newComment } = this.state;
    fetch(commentsUrl, {
      credentials: "same-origin",
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newComment)
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState(prevState => ({
          newComment: "",
          comments: prevState.comments.concat(data)
        }));
      })
      .catch((error) => console.log(error));
  }

  likeClick(likeOnly) {
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
    else if (!likeOnly) {
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
      postShowUrl, newComment } = this.state;
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
          <img src={imgUrl} alt={imgUrl} onDoubleClick={() => this.likeClick(true)} />
        </div>
        <div>
          <div>
            <button
              type='button'
              className="like-unlike-button"
              onClick={() => this.likeClick(false)}
            >
              {lognameLikesThis ? "unlike" : "like"}
            </button>
          </div>
          <div>
            {numLikes}
            {numLikes === 1 ? " like" : " likes"}
          </div>
        </div>
        {
          comments.map((comment) => (
            <div>
              <div>
                <a href={comment.ownerShowUrl}>
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
            </div>
          ))
        }
        <div>
          <form
            className="comment-form"
            onSubmit={(e) => { this.handleSubmit(e, commentsUrl) }}
          >
            <input
              type="text"
              value={newComment}
              onChange={this.handleChange}
            />
          </form>
        </div >
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
