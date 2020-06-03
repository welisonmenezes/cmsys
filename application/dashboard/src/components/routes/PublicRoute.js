import React from "react";
import { Route, Redirect } from "react-router-dom";
import IsLoggedIn from "../../utils/auth/IsLoggedIn";

const PublicRoute = ({ component: Component, restricted, ...rest }) => {
    return (
        <Route
            {...rest}
            render={(props) =>
                IsLoggedIn() && restricted ? (
                    <Redirect to="/dashboard" />
                ) : (
                    <Component {...props} />
                )
            }
        />
    );
};

export default PublicRoute;
