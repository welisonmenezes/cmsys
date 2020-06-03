import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import "./App.scss";
import AppProvider from "./contexts/AppContext";
import PublicRoute from "./components/routes/PublicRoute";
import PrivateRoute from "./components/routes/PrivateRoute";
import SignIn from "./components/auth/SignIn";
import Dashboard from "./components/dashboard/Dashboard";
import Error404 from "./components/error/Error404";

const App = () => {
    return (
        <div className="App">
            <AppProvider>
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
            </AppProvider>
        </div>
    );
};

export default App;
