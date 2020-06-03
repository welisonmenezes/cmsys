import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "./App.scss";
import PublicRoute from "./components/routes/PublicRoute";
import PrivateRoute from "./components/routes/PrivateRoute";
import SignIn from "./components/auth/SignIn";
import Dashboard from "./components/dashboard/Dashboard";
import Error404 from "./components/error/Error404";

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Switch>
                    <PublicRoute
                        restricted={true}
                        component={SignIn}
                        path="/"
                        exact
                    />
                    <PrivateRoute component={Dashboard} path="/dashboard" />
                    <Route component={Error404} />
                </Switch>
            </BrowserRouter>
        </div>
    );
}

export default App;
