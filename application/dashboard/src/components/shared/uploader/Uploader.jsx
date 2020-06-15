import React, { useState, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import UploaderFiles from "./UploaderFiles";
import UploaderModal from "./UploaderModal";
import "./Uploader.scss";

const Uploader = () => {
    const [files, setFiles] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [preview, setPreview] = useState(null);

    const {
        getRootProps,
        getInputProps,
        isDragActive,
        isDragAccept,
        isDragReject,
    } = useDropzone({
        accept: ["image/*", "application/pdf"],
        onDrop: (acceptedFiles) => {
            acceptedFiles.map(async (file) => {
                //console.log(file)
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
                            type: file.type
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

    const openUploaderModal = (file) => {
        setShowModal(true);
        setPreview(file);
    };

    const closeUploaderModal = () => {
        setShowModal(false);
        setPreview(null);
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
                openUploaderModal={openUploaderModal}
            />
            <UploaderModal
                showModal={showModal}
                closeUploaderModal={closeUploaderModal}
                file={preview}
            />
        </div>
    );
};

export default Uploader;
