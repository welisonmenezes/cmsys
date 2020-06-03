import React, { useContext } from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { AppContext } from "../../../contexts/AppContext";

const MainMenu = () => {
    const { url } = useRouteMatch();
    const { layoutState } = useContext(AppContext);

    return (
        <div className={`MainMenu noselect ${layoutState.isMenuOpen ? "menu-opened" : ""}`}>
            <Link to={`${url}/post`}>Post</Link>
        </div>
    );
}

export default MainMenu;
