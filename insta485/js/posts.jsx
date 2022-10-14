import React from "react";
import PropTypes from "prop-types";
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from "./post";

class Posts extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            next: "",
            results: [],
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
                    next: data.next,
                    results: data.results,
                });
            })
            .catch((error) => console.log(error));
    }

    extend() {
        const { next } = this.state;
        fetch(next, { credentials: "same-origin" })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                this.setState(prevState => ({
                    next: data.next,
                    results: [...prevState.results, ...data.results],
                }));
            })
            .catch((error) => console.log(error));
    }

    render() {
        const { next, results } = this.state;
        console.log(next, results);
        return (
            <InfiniteScroll
                dataLength={results.length}
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
                    results.map((post) => (
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
