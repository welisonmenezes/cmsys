import React, { useState, createContext } from "react";

export const AppContext = createContext();

const AppProvider = ({ children }) => {
    const [layoutState, setLayoutState] = useState({
        isMenuOpen: true,
    });

    return (
        <AppContext.Provider value={{ layoutState, setLayoutState }}>
            { children }
        </AppContext.Provider>
    );
};

export default AppProvider;
