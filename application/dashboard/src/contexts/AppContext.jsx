import React, { useState, createContext, useEffect } from "react";

export const AppContext = createContext();

const AppProvider = ({ children }) => {
    const getLocalStorageMenuStatus = () => {
        const status = localStorage.getItem("isMenuOpen");
        return status && status === "true" ? true : false;
    };

    const [layoutState, setLayoutState] = useState({
        isMenuOpen: getLocalStorageMenuStatus(),
    });

    useEffect(() => {
        localStorage.setItem("isMenuOpen", layoutState.isMenuOpen);
    }, [layoutState.isMenuOpen]);

    return (
        <AppContext.Provider value={{ layoutState, setLayoutState }}>
            {children}
        </AppContext.Provider>
    );
};

export default AppProvider;
