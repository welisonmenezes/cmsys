import React from "react";
import { IoMdCreate, IoIosCloseCircle, IoMdCloudUpload } from "react-icons/io";
import "./UploaderFiles.scss";
import { FormatBytes } from "../../../utils/FileUtils";

const UploaderFiles = (props) => {
    return (
        <div className="UploaderFiles">
            {props.files.map((file) => (
                <div key={file.key}>
                    <div className="thumb-grid d-flex justify-content-around align-items-center">
                        <div>
                            <div className="thumb-item">
                                <div onClick={() => {props.openModalImagePreview(file)}}>
                                    <img src={file.preview} alt="" />
                                </div>
                            </div>
                        </div>
                        <div className="ellipse-text">
                            <span>{file.name}</span>
                        </div>
                        <div className="ellipse-text">
                            <span>{FormatBytes(file.size)}</span>
                        </div>
                        <div>
                            <button
                                className="btn btn-sm btn-primary"
                                onClick={() => props.uploadFile(file)}
                            >
                                <IoMdCloudUpload /> Enviar
                            </button>
                            <button
                                className="btn btn-sm btn-success"
                                onClick={() => props.editFile(file)}
                            >
                                <IoMdCreate /> Editar
                            </button>
                            <button
                                className="btn btn-sm btn-danger"
                                onClick={() => props.removeFile(file.key)}
                            >
                                <IoIosCloseCircle />
                                Cancelar
                            </button>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default UploaderFiles;
