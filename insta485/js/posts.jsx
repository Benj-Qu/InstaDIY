import React from "react";
import PropTypes from "prop-types";
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from "./post";

class Posts extends React.Component {
    /* Display image and post owner of a single post
     */
    constructor(props) {
        // Initialize mutable state
        super(props);
        this.state = {
            next: "",
            posts: []
        };
    }

    componentDidMount() {
        // This line automatically assigns this.props.url to the const variable url
        const { url } = this.props;
        // Call REST API to get the post's information
        fetch(url, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState({
                    next: data.next,
                    posts: data.posts,
                });
            })
            .catch((error) => console.log(error));
    }

    extend() {
        // This line automatically assigns this.props.url to the const variable url
        const { posts, next } = this.state;
        // Call REST API to get the post's information
        fetch(next, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState({
                    next: data.next,
                    posts: [...posts, ...data.posts],
                });
            })
            .catch((error) => console.log(error));
    }

    render() {
        // This line automatically assigns this.state.imgUrl to the const variable imgUrl
        // and this.state.owner to the const variable owner
        const { next, posts } = this.state;
        // Render post image and post owner
        return (
            <InfiniteScroll
                dataLength={posts.length}
                next={() => this.extend()}
                hasMore={next !== ""}
                loader={<h4>Loading...</h4>}
                endMessage={
                    <p style={{ textAlign: 'center' }}>
                        <b>Yay! You have seen it all</b>
                    </p>
                }
            >
                {
                    posts.map((post) => (
                        <Post url={post.url} />
                    ))
                }
            </InfiniteScroll>
        );
    }
}
Posts.propTypes = {
    url: PropTypes.string.isRequired,
};
export default Posts;
