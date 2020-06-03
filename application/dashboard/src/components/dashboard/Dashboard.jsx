import React, { useContext } from "react";
import { Switch, Route, useRouteMatch } from "react-router-dom";
import "./Dashboard.scss";
import { AppContext } from "../../contexts/AppContext";
import TopBar from "../shared/top-bar/TopBar";
import MainMenu from "../shared/main-menu/MainMenu";
import Post from "../pages/Posts";

const Dashboard = () => {
    const { url } = useRouteMatch();
    const { layoutState } = useContext(AppContext);

    console.log(layoutState)

    return (
        <div className={`Dashboard ${layoutState.isMenuOpen ? "menu-opened" : ""}`}>
            <header>
                <TopBar></TopBar>
            </header>
            <section className="d-flex">
                <aside className="nice-transition-width">
                    <MainMenu></MainMenu>
                </aside>
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
