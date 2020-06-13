import React, { useState } from "react";
import { Modal } from "react-bootstrap";
import { useEffect } from "react";
import "./UploaderEditImage.scss";

const UploaderEditImage = (prop) => {
    const [show, setShow] = useState(false);

    useEffect(() => {
        setShow(prop.showModal);
    }, [prop.showModal]);

    const showPreview = () => {
        if (prop.file) {
            return (
                <img src={prop.file.preview} alt="" />
            );
        }
    };

    return (
        <>
            <Modal
                className="UploaderImageModal"
                show={show}
                onHide={prop.closeModalImagePreview}
                animation={false}
            >
                <Modal.Header closeButton>
                    <Modal.Title className="ellipse-text">{prop.file?.name}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {showPreview()}
                </Modal.Body>
            </Modal>
        </>
    );
};

export default UploaderEditImage;
