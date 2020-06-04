import React, { useContext } from "react";
import { useRouteMatch, NavLink } from "react-router-dom";
import {
    IoMdListBox,
    IoMdFolder,
    IoIosSettings,
    IoMdPaper,
    IoMdPeople,
} from "react-icons/io";
import "./MainMenu.scss";
import { AppContext } from "../../../contexts/AppContext";
import logo from "../../../images/welison-menezes-logo.png";

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
            <figure className="fig-logo">
                <img src={logo} alt="WM Logo" />
                Manager
            </figure>
            <ul>
                <li>
                    <NavLink to={`${url}/posts`} onClick={toogleMenu}>
                        <IoMdListBox /> <span>Posts</span>
                    </NavLink>
                </li>
                <li>
                    <NavLink to={`${url}/medias`} onClick={toogleMenu}>
                        <IoMdFolder /> <span>Arquivos</span>
                    </NavLink>
                </li>

                <li>
                    <NavLink to={`${url}/post-types`} onClick={toogleMenu}>
                        <IoMdPaper /> <span>Tipos de Post</span>
                    </NavLink>
                </li>
                <li>
                    <NavLink to={`${url}/users`} onClick={toogleMenu}>
                        <IoMdPeople /> <span>Usuários</span>
                    </NavLink>
                </li>
                <li>
                    <NavLink
                        to={`${url}/configurations`}
                        onClick={toogleMenu}
                        activeClassName="active"
                    >
                        <IoIosSettings /> <span>Configurações</span>
                    </NavLink>
                </li>
            </ul>
        </div>
    );
};

export default MainMenu;
