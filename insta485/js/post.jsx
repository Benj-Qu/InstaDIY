import React from "react";
import PropTypes from "prop-types";
import moment from "moment";
import Like from "./like";

class Post extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      comments: {},
      comments_url: "",
      created: "",
      imgUrl: "",
      likes: "",
      owner: "",
      ownerImgUrl: "",
      ownerShowUrl: "",
      postShowUrl: "",
      postid: -1
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
          comments_url: data.comments_url,
          created: data.created,
          imgUrl: data.imgUrl,
          likes: data.likes,
          owner: data.owner,
          ownerImgUrl: data.ownerImgUrl,
          ownerShowUrl: data.ownerShowUrl,
          postShowUrl: data.postShowUrl,
          postid: data.postid
        });
      })
      .catch((error) => console.log(error));
  }

  render() {
    const { comments, comments_url, created, imgUrl,
      likes, owner, ownerImgUrl, ownerShowUrl,
      postShowUrl, postid } = this.state;
    const { timestamp } = created.now();
    return (
      <div>
        <div>
          <a href={ownerShowUrl}>
            <img src={ownerimgurl} alt={owner} />
            <div> {owner} </div>
          </a>
        </div>
        <div>
          <a href={postShowUrl}>{timestamp}</a>
        </div>
        <div>
          <img src={imgUrl} alt={imgUrl} />
        </div>
        <Like likes={likes} />
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
