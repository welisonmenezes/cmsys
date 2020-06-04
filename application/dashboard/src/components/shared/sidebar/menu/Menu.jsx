import React, { useContext } from "react";
import { useRouteMatch, NavLink } from "react-router-dom";
import {
    IoMdListBox,
    IoMdFolder,
    IoIosSettings,
    IoMdPaper,
    IoMdPeople,
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
        closeAllSubmenus();
        if (e.currentTarget.classList.contains('active')) {
            e.currentTarget.classList.remove('active');
        } else {
            e.currentTarget.classList.add('active');
        }
    }

    const closeAllSubmenus = () => {
        let submenus = document.querySelectorAll('.menu-header');
        if (submenus) {
            for (let i = 0; i < submenus.length; i++) {
                submenus[i].classList.remove('active');
            }
        }
    }

    return (
        <ul className="Menu">
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
            <li>
                <NavLink
                    to={`${url}/configurations`}
                    onClick={closeMenu}
                    activeClassName="active"
                >
                    <IoIosSettings /> <span>Configurações</span>
                </NavLink>
            </li>
        </ul>
    );
};

export default Menu;
