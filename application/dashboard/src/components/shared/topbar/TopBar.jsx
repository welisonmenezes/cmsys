import React, { useContext } from "react";
import { IoIosMenu, IoIosArrowRoundBack } from "react-icons/io";
import { AppContext } from "../../../contexts/AppContext";
import "./TopBar.scss";

const TopBar = () => {
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
        <div
            className={`TopBar d-flex align-items-center ${
                layoutState.isMenuOpen ? "menu-opened" : ""
            }`}
        >
            <ul className="d-flex align-items-center menu-icons">
                {layoutState.isMenuOpen && (
                    <li>
                        <span
                            className="btn-icon nice-transition"
                            onClick={toogleMenu}
                        >
                            <IoIosArrowRoundBack />
                        </span>
                    </li>
                )}
                {! layoutState.isMenuOpen && (
                    <li>
                        <span
                            className="btn-icon nice-transition"
                            onClick={toogleMenu}
                        >
                            <IoIosMenu />
                        </span>
                    </li>
                )}
            </ul>
        </div>
    );
};

export default TopBar;
