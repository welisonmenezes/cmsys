import React, { useState } from "react";
import { useDropzone } from "react-dropzone";

const Uploader = () => {
    const [files, setFiles] = useState([]);

    const { getRootProps, getInputProps } = useDropzone({
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

    const thumbs = files.map((file) => (
        <div key={file.key}>
            <div>
                <img src={file.preview} alt="" />
            </div>
        </div>
    ));

    return (
        <div>
            <div {...getRootProps({ className: "dropzone" })}>
                <input {...getInputProps()} />
                <p>Drag 'n' drop some files here, or click to select files</p>
            </div>
            <aside>{thumbs}</aside>
        </div>
    );
};

export default Uploader;
