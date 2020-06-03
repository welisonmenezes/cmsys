import React from 'react';
import { Switch, Route, useRouteMatch } from 'react-router-dom';
import './Dashboard.scss';
import TopBar from '../shared/top-bar/TopBar';
import MainMenu from '../shared/main-menu/MainMenu';
import Post from '../pages/Posts';

function Dashboard() {

    let { url } = useRouteMatch();

    console.log(url)

    return (
        <div className="Dashboard">
            <header>
                <TopBar></TopBar>
            </header>
            <section className="d-flex">
                <aside>
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
}

export default Dashboard;
