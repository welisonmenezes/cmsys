import React, { useContext } from "react";
import "./Sidebar.scss";
import { AppContext } from "../../../contexts/AppContext";
import logo from "../../../images/welison-menezes-logo.png";
import Menu from "./menu/Menu";

const Sidebar = () => {
    const { layoutState } = useContext(AppContext);

    return (
        <div
            className={`Sidebar noselect ${
                layoutState.isMenuOpen ? "menu-opened" : ""
            }`}
        >
            <figure className="fig-logo d-flex nice-transition">
                <img src={logo} alt="WM Logo" />
                <span>CMSYS</span>
            </figure>
            <Menu />
        </div>
    );
};

export default Sidebar;
