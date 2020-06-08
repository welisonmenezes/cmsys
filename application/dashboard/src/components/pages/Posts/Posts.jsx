import React from "react";
import WMEditor from "../../shared/editor/WMEditor";
import Uploader from "../../shared/uploader/Uploader";

const Posts = () => {
    return (
        <div className="Posts">
            <h1>Página de Posts</h1>
            <Uploader />
            <WMEditor />
        </div>
    );
}

export default Posts;
