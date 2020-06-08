import React, { useState, useMemo } from "react";
import { useDropzone } from "react-dropzone";

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
            acceptedFiles.map((file) => {
                var reader = new window.FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = async function () {
                    const base64data = reader.result;
                    setFiles([...files, { preview: base64data, key: "xxx" }]);
                };
                return true;
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

    const thumbs = files.map((file) => (
        <div key={file.key}>
            <div>
                <img src={file.preview} alt="" />
            </div>
        </div>
    ));

    return (
        <div>
            <div {...getRootProps({ style })}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
            <aside>{thumbs}</aside>
        </div>
    );
};

export default Uploader;
