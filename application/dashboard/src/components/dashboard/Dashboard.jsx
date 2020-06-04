import React, { useContext } from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";
import "./Dashboard.scss";
import { AppContext } from "../../contexts/AppContext";
import TopBar from "../shared/top-bar/TopBar";
import MainMenu from "../shared/main-menu/MainMenu";
import Post from "../pages/Posts";

const Dashboard = () => {
    const { url } = useRouteMatch();
    const { layoutState, setLayoutState } = useContext(AppContext);

    const toogleMenu = (e) => {
        e.preventDefault();
        if (layoutState.isMenuOpen) {
            setLayoutState({ ...layoutState, isMenuOpen: false });
        } else {
            setLayoutState({ ...layoutState, isMenuOpen: true });
        }
    };

    return (
        <div className={`Dashboard ${layoutState.isMenuOpen ? "menu-opened" : ""}`}>
            <header>
                <TopBar></TopBar>
            </header>
            <section className="d-flex">
                <aside className="nice-transition nt-left-width">
                    <MainMenu></MainMenu>
                </aside>
                <div className="mbl-overlay-menu nice-transition" onClick={toogleMenu}></div>
                <main>
                    <Switch>
                        <Route exact path={`${url}/post`} component={Post} />
                    </Switch>
                </main>
            </section>
        </div>
    );
};

export default Dashboard;
