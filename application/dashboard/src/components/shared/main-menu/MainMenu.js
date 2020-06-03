import React from "react";
import { Link, useRouteMatch } from "react-router-dom";

function MainMenu() {
    let { url } = useRouteMatch();

    return (
        <div className="MainMenu">
            <Link to={`${url}/post`}>Post</Link>
        </div>
    );
}

export default MainMenu;
