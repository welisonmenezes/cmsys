import React from "react";
import { Redirect } from "react-router-dom";
import IsLoggedIn from "../../utils/auth/IsLoggedIn";

const SignIn = () => {
    const renderRedirect = () => {
        if (this.state.redirect) {
            return <Redirect to="/dashboard" />;
        }
    };

    return (
        <div className="SignIn">
            {IsLoggedIn() && renderRedirect()}

            {!IsLoggedIn() && (
                <>
                    <h1>Login page</h1>
                </>
            )}
        </div>
    );
};

export default SignIn;
