import React from "react";
import PDFIcon from "./icons/pdf.svg";

const UploaderPreview = ({ file, origin }) => {
    const fileTypes = [
        "image/png",
        "image/jpg",
        "image/jpeg",
        "image/gif",
        "image/svg",
    ];

    const showPreview = () => {
        if (file) {
            if (fileTypes.includes(file.type))
                return <img src={file.preview} alt="File Preview" />;
            else if (file.type === "application/pdf") {
                if (origin === "list") {
                    return <img src={PDFIcon} alt="PDF Preview" />;
                }
                return <object data={file.preview} type="application/pdf">{file.name}</object>;
            }
        }
        return null;
    };

    return showPreview();
};

export default UploaderPreview;
