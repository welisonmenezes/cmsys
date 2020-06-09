import React from "react";

const thumbsContainer = {
    display: "flex",
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 16,
};

const thumb = {
    display: "inline-flex",
    borderRadius: 2,
    border: "1px solid #eaeaea",
    marginBottom: 8,
    marginRight: 8,
    width: 100,
    height: 100,
    padding: 4,
    boxSizing: "border-box",
};

const thumbInner = {
    display: "flex",
    minWidth: 0,
    overflow: "hidden",
};

const img = {
    display: "block",
    width: "auto",
    height: "100%",
};

const UploaerThumb = (props) => {

    const thumbs = props.files.map((file) => (
        <div style={thumb} key={file.key}>
            <div style={thumbInner}>
                <img style={img} src={file.preview} alt="" />
            </div>
        </div>
    ));

    return (
        <div style={thumbsContainer} className="UploaerThumb">
            {thumbs}
        </div>
    );
};

export default UploaerThumb;
