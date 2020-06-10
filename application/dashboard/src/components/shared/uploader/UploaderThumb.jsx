import React from "react";
import "./UploaderThumb.scss";

const UploaerThumb = (props) => {

    const thumbs = props.files.map((file) => (
        <div className="thumb-item" key={file.key}>
            <div>
                <img src={file.preview} alt="" />
            </div>
        </div>
    ));

    return (
        <div className="UploaerThumb">
            {thumbs}
        </div>
    );
};

export default UploaerThumb;
