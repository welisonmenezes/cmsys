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
        const { innerWidth: width } = window;
        if (width <= 992) {
            disableAnimationTemporarily();
            setLayoutState({ ...layoutState, isMenuOpen: false });
        }
        hideMenuAtNarrowScreenOnResize();
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    const disableAnimationTemporarily = () => {
        const bg = document.querySelector(".Dashboard .mbl-overlay-menu");
        const aside = document.querySelector(".Dashboard > section > aside");
        if (bg && aside) {
            bg.classList.remove("nice-transition");
            aside.classList.remove("nice-transition");
            setTimeout(() => {
                bg.classList.add("nice-transition");
                aside.classList.add("nice-transition");
            }, 10);
        }
    };

    const hideMenuAtNarrowScreenOnResize = () => {
        window.addEventListener("resize", () => {
            const { innerWidth: width } = window;
            const dashboard = document.querySelector(".Dashboard.menu-opened");
            if (width <= 992 && dashboard) {
                disableAnimationTemporarily();
                setLayoutState({ ...layoutState, isMenuOpen: false });
            } else {
                disableAnimationTemporarily();
            }
        });
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
