import React from "react";
import PropTypes from "prop-types";

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
    let owner_img_url = "/uploads/{}".format(ownerImgUrl);
    // Render post image and post owner
    return (
      <div>
        <a href="/users/{owner}/">
          <img src={owner_img_url} alt={owner} />
          <div> {owner} </div>
        </a>
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
