import React, { useState, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import UploaerThumb from "./UploaderThumb";

const baseStyle = {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    padding: "20px",
    borderWidth: 2,
    borderRadius: 2,
    borderColor: "#798699",
    borderStyle: "dashed",
    backgroundColor: "#FFFFFF",
    color: "#798699",
    outline: "none",
    transition: "border .24s ease-in-out",
};

const activeStyle = {
    borderColor: "#009efb",
};

const acceptStyle = {
    borderColor: "#009efb",
};

const rejectStyle = {
    borderColor: "#ff1744",
};

const Uploader = () => {
    const [files, setFiles] = useState([]);

    const {
        getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject,
    } = useDropzone({
        accept: "image/*",
        onDrop: (acceptedFiles) => {
            acceptedFiles.map(async (file) => {
                console.log(file)
                var reader = new window.FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = function () {
                    const base64data = reader.result;
                    setFiles(files => [
                        ...files,
                        {
                            preview: base64data,
                            key: new Date().getMilliseconds(),
                        },
                    ]);
                };
            });
        },
    });

    const style = useMemo(
        () => ({
            ...baseStyle,
            ...(isDragActive ? activeStyle : {}),
            ...(isDragAccept ? acceptStyle : {}),
            ...(isDragReject ? rejectStyle : {}),
        }),
        [isDragActive, isDragReject, isDragAccept]
    );

    return (
        <div>
            <div {...getRootProps({ style })}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
            <UploaerThumb files={files} />
        </div>
    );
};

export default Uploader;
