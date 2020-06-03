import React from "react";
import { Route, Redirect } from "react-router-dom";
import IsLoggedIn from "../../utils/auth/IsLoggedIn";

const PrivateRoute = ({ component: Component, ...rest }) => {
    return (
        <Route
            {...rest}
            render={(props) =>
                IsLoggedIn() ? <Component {...props} /> : <Redirect to="/" />
            }
        />
    );
};

export default PrivateRoute;
