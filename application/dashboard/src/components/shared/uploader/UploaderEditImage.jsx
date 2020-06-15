import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import { useEffect } from "react";
import "./UploaderEditImage.scss";

const UploaderEditImage = ({ showModal, file, closeModalImagePreview }) => {
    const [show, setShow] = useState(false);

    useEffect(() => {
        setShow(showModal);
    }, [showModal]);

    const showPreview = () => {
        if (file) {
            return <img src={file.preview} alt="" />;
        }
    };

    return (
        <>
            <Modal
                className="UploaderImageModal"
                show={show}
                onHide={closeModalImagePreview}
                animation={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title className="ellipse-text">
                        {file?.name}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>{showPreview()}</Modal.Body>
            </Modal>
        </>
    );
};

export default UploaderEditImage;
