import React, { useContext, useEffect } from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";
import "./Dashboard.scss";
import { AppContext } from "../../contexts/AppContext";
import TopBar from "../shared/topbar/TopBar";
import Sidebar from "../shared/sidebar/Sidebar";
import Configurations from "../pages/Configurations/Configurations";
import Medias from "../pages/Medias/Medias";
import Posts from "../pages/Posts/Posts";
import PostTypes from "../pages/PostTypes/PostTypes";
import Users from "../pages/Users/Users";

const Dashboard = () => {
    const { url } = useRouteMatch();
    const { layoutState, setLayoutState } = useContext(AppContext);

    useEffect(() => {
        hideMenuAtNarrowScreen();
        window.addEventListener("resize", () => {
            hideMenuAtNarrowScreen();
        });
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        if (layoutState.isMenuOpen) {
            const sidebar = document.querySelector(
                ".Dashboard > section > aside"
            );
            if (sidebar) {
                console.log("sexo");
                sidebar.scrollTop = 0;
            }
        }
    }, [layoutState]);

    const disableAnimationTemporarily = () => {
        const bg = document.querySelector(".Dashboard .mbl-overlay-menu");
        const aside = document.querySelector(".Dashboard > section > aside");
        if (bg && aside) {
            bg.classList.remove("nice-transition");
            aside.classList.remove("nice-transition");
            setTimeout(() => {
                bg.classList.add("nice-transition");
                aside.classList.add("nice-transition");
            }, 1);
        }
    };

    const hideMenuAtNarrowScreen = () => {
        const { innerWidth: width } = window;
        const dashboard = document.querySelector(".Dashboard.menu-opened");
        disableAnimationTemporarily();
        if (width <= 992 && dashboard) {
            setLayoutState({ ...layoutState, isMenuOpen: false });
        }
    };

    const closeMenu = () => {
        setLayoutState({ ...layoutState, isMenuOpen: false });
    };

    return (
        <div
            className={`Dashboard ${
                layoutState.isMenuOpen ? "menu-opened" : ""
            }`}
        >
            <header>
                <TopBar></TopBar>
            </header>
            <section className="d-flex">
                <aside className="nice-transition nt-left-width">
                    <Sidebar></Sidebar>
                </aside>
                <div
                    className="mbl-overlay-menu nice-transition"
                    onClick={closeMenu}
                ></div>
                <main>
                    <Switch>
                        <Route
                            exact
                            path={`${url}/configurations`}
                            component={Configurations}
                        />
                        <Route
                            exact
                            path={`${url}/medias`}
                            component={Medias}
                        />
                        <Route exact path={`${url}/posts`} component={Posts} />
                        <Route
                            exact
                            path={`${url}/post-types`}
                            component={PostTypes}
                        />
                        <Route exact path={`${url}/users`} component={Users} />
                    </Switch>
                </main>
            </section>
        </div>
    );
};

export default Dashboard;
