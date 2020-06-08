import React, { useContext } from "react";
import { useRouteMatch, NavLink } from "react-router-dom";
import {
    IoMdListBox,
    IoMdFolder,
    IoIosSettings,
    IoMdPaper,
    IoMdPeople,
    IoIosHome,
} from "react-icons/io";
import "./Menu.scss";
import { AppContext } from "../../../../contexts/AppContext";

const Menu = () => {
    const { url } = useRouteMatch();
    const { layoutState, setLayoutState } = useContext(AppContext);

    const closeMenu = (e) => {
        const { innerWidth: width } = window;
        if (width <= 992) {
            setLayoutState({ ...layoutState, isMenuOpen: false });
        }
    };

    const toggleSubmenu = (e) => {
        e.preventDefault();
        const el = e.currentTarget;
        const { innerWidth: width } = window;
        if (
            el.parentElement.parentElement.classList.contains("menu-closed") &&
            width > 992
        ) {
            return;
        }

        closeAllSubmenus();

        if (el.classList.contains("active")) {
            el.classList.remove("active");
        } else {
            el.classList.add("active");
        }
    };

    const closeAllSubmenus = () => {
        let submenus = document.querySelectorAll(".menu-header");
        if (submenus) {
            for (let i = 0; i < submenus.length; i++) {
                const active = submenus[i].parentElement.querySelector('.submenu a.active');
                if (! active)
                {
                    submenus[i].classList.remove("active");
                }
            }
        }
    };

    const isShortFreeHeight = (menu) => {
        const { innerHeight: height } = window;
        const freeHeight = height - 60 - 70 - 80;
        const elHeight = menu.offsetHeight;
        if (freeHeight < elHeight) {
            if (!layoutState.isMenuOpen) {
                menu.parentElement.parentElement.classList.add("was-closed");
                
            }
            menu.parentElement.parentElement.classList.add("overflowed");
            return true;
        }
        menu.parentElement.parentElement.classList.remove("overflowed");
        return false;
    };

    const openMenuAtShortScreen = (e) => {
        const menu = document.querySelector(".Menu");
        if (menu && isShortFreeHeight(menu)) {
            setLayoutState({ ...layoutState, isMenuOpen: true });
        }
    };

    const closeMenuAtShortScreen = (e) => {
        const menu = document.querySelector(".Menu");
        if (menu) {
            const parent = menu.parentElement.parentElement;
            if (parent && parent.classList.contains("was-closed")) {
                parent.classList.remove("was-closed");
                setLayoutState({ ...layoutState, isMenuOpen: false });
                closeAllSubmenus();
            }
        }
    };

    return (
        <ul
            className={`Menu ${
                layoutState.isMenuOpen ? "menu-opened" : "menu-closed"
            }`}
            onMouseLeave={closeMenuAtShortScreen}
            onMouseEnter={openMenuAtShortScreen}
        >
            <li>
                <NavLink
                    to={`${url}`}
                    onClick={closeMenu}
                    activeClassName="active"
                    className="menu-root"
                    exact
                >
                    <IoIosHome /> <span>Home</span>
                </NavLink>
            </li>
            <li>
                <NavLink
                    to={`${url}/posts`}
                    onClick={toggleSubmenu}
                    activeClassName="active"
                    className="menu-header"
                >
                    <IoMdListBox /> <span>Posts</span>
                </NavLink>
                <ul className="submenu nice-transition">
                    <li>
                        <NavLink
                            to={`${url}/posts`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Ver Todos
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to={`${url}/posts`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Criar Novo
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to={`${url}/posts`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Ver Categorias
                        </NavLink>
                    </li>
                </ul>
            </li>
            <li>
                <NavLink
                    to={`${url}/medias`}
                    onClick={toggleSubmenu}
                    activeClassName="active"
                    className="menu-header"
                >
                    <IoMdFolder /> <span>Arquivos</span>
                </NavLink>
                <ul className="submenu nice-transition">
                    <li>
                        <NavLink
                            to={`${url}/medias`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Ver Todos
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to={`${url}/medias`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Enviar Novo
                        </NavLink>
                    </li>
                </ul>
            </li>
            <li>
                <NavLink
                    to={`${url}/post-types`}
                    onClick={toggleSubmenu}
                    activeClassName="active"
                    className="menu-header"
                >
                    <IoMdPaper /> <span>Tipos de Post</span>
                </NavLink>
                <ul className="submenu nice-transition">
                    <li>
                        <NavLink
                            to={`${url}/post-types`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Ver Todos
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to={`${url}/post-types`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Criar Novo
                        </NavLink>
                    </li>
                </ul>
            </li>
            <li>
                <NavLink
                    to={`${url}/configurations`}
                    onClick={closeMenu}
                    activeClassName="active"
                    className="menu-root"
                >
                    <IoIosSettings /> <span>Configurações</span>
                </NavLink>
            </li>
            <li>
                <NavLink
                    to={`${url}/users`}
                    onClick={toggleSubmenu}
                    activeClassName="active"
                    className="menu-header"
                >
                    <IoMdPeople /> <span>Usuários</span>
                </NavLink>
                <ul className="submenu nice-transition">
                    <li>
                        <NavLink
                            to={`${url}/users`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Ver Todos
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to={`${url}/users`}
                            onClick={closeMenu}
                            activeClassName="active"
                        >
                            Adicionar Novo
                        </NavLink>
                    </li>
                </ul>
            </li>
        </ul>
    );
};

export default Menu;
