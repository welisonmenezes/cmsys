import React, { useContext } from "react";
import "./MainMenu.scss";
import { Link, useRouteMatch } from "react-router-dom";
import { AppContext } from "../../../contexts/AppContext";

const MainMenu = () => {
    const { url } = useRouteMatch();
    const { layoutState, setLayoutState } = useContext(AppContext);

    const toogleMenu = (e) => {
        const { innerWidth: width } = window;

        if (width <= 992) {
            if (layoutState.isMenuOpen) {
                setLayoutState({ ...layoutState, isMenuOpen: false });
            } else {
                setLayoutState({ ...layoutState, isMenuOpen: true });
            }
        }
    };

    return (
        <div
            className={`MainMenu noselect ${
                layoutState.isMenuOpen ? "menu-opened" : ""
            }`}
        >
            <Link to={`${url}/post`} onClick={toogleMenu}>
                Post
            </Link>
        </div>
    );
};

export default MainMenu;
