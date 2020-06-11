import React, { useState, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import UploaderFiles from "./UploaderFiles";
import "./Uploader.scss";

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
                var reader = new window.FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = function () {
                    const base64data = reader.result;
                    setFiles((files) => [
                        ...files,
                        {
                            preview: base64data,
                            key: new Date().getMilliseconds(),
                            name: file.name,
                            size: file.size,
                        },
                    ]);
                };
            });
        },
    });

    const theClass = useMemo(() => {
        let className = "area";
        if (isDragActive) {
            className += " drag-active";
        }
        if (isDragReject) {
            className += " drag-reject";
        }
        if (isDragAccept) {
            className += " drag-accept";
        }
        return className;
    }, [isDragActive, isDragReject, isDragAccept]);

    const removeFile = (key) => {
        const newFiles = files.filter((file) => file.key !== key);
        setFiles(newFiles);
    };

    const uploadFile = (file) => {
        console.log("Uploading the file: ", file);
    };

    const editFile = (file) => {
        console.log("Editing the file: ", file);
    };

    return (
        <div className="Uploader">
            <div {...getRootProps({ className: theClass })}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
            <UploaderFiles
                files={files}
                removeFile={removeFile}
                uploadFile={uploadFile}
                editFile={editFile}
            />
        </div>
    );
};

export default Uploader;
